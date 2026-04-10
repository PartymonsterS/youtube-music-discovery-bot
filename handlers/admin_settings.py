from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from config import ADMIN_ID
from services.settings_service import load_settings
from keyboards.admin_keyboard import admin_keyboard
from keyboards.main_keyboard import main_keyboard
from youtube_music import ym_client

router = Router()


@router.message(Command("admin"))
async def admin_panel_handler(message: Message):
    if str(message.from_user.id) != ADMIN_ID:
        return

    await message.answer(
        "⚙️ <b>Admin Panel</b>",
        parse_mode="HTML",
        reply_markup=admin_keyboard
    )


@router.callback_query(F.data == "admin_show_settings")
async def admin_show_settings_handler(callback: CallbackQuery):
    if str(callback.from_user.id) != ADMIN_ID:
        return

    settings = load_settings()

    await callback.message.answer(
        "⚙️ <b>Текущие настройки</b>\n\n"
        f"owner: <b>{settings['owner']}</b>\n"
        f"admin_id: <b>{settings['admin_id']}</b>\n"
        f"random_playlist_size: <b>{settings['random_playlist_size']}</b>\n"
        f"playlist_search_max_count: <b>{settings['playlist_search_max_count']}</b>\n"
        f"music_flow_search_limit: <b>{settings['music_flow_search_limit']}</b>",
        parse_mode="HTML"
    )

    await callback.answer()

@router.callback_query(F.data == "admin_full_sync")
async def admin_full_sync_handler(callback: CallbackQuery):
    if str(callback.from_user.id) != ADMIN_ID:
        return

    await callback.message.answer("⏳ Секунду, подождите... Синхронизирую библиотеку 🎧")

    try:
        ym_client.connect()
        result = ym_client.full_sync()

        await callback.message.answer(
            "Синхронизация завершена ✅\n\n"
            "В библиотеке найдено:\n"
            f"🎵 {result['total']} треков",
            reply_markup=main_keyboard
        )
    except Exception as e:
        await callback.message.answer(f"Ошибка: {e}")

    await callback.answer()


@router.callback_query(F.data == "admin_sync_new")
async def admin_sync_new_handler(callback: CallbackQuery):
    if str(callback.from_user.id) != ADMIN_ID:
        return

    await callback.message.answer("⏳ Секунду, подождите... Проверяю новые треки 🎧")

    try:
        ym_client.connect()
        result = ym_client.sync_new()

        await callback.message.answer(
            "Обновление завершено ✅\n\n"
            f"Добавлено новых треков: {result['added']}\n"
            f"Всего треков: {result['total']}",
            reply_markup=main_keyboard
        )
    except Exception as e:
        await callback.message.answer(f"Ошибка: {e}")

    await callback.answer()