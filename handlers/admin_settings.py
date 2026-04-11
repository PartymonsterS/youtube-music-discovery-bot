from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from config import ADMIN_ID
from services.settings_service import load_settings
from keyboards.admin_keyboard import admin_keyboard
from keyboards.main_keyboard import main_keyboard
from youtube_music import ym_client

from aiogram.fsm.context import FSMContext

from services.yt_auth_service import set_yt_auth_value
from states.yt_auth import YTAuthState

from aiogram import F
from aiogram.types import CallbackQuery

from services.yt_auth_service import set_yt_auth_value
from states.yt_auth import YTAuthState
from keyboards.back_to_menu_keyboard import back_to_menu_keyboard

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

@router.callback_query(F.data == "admin_set_cookie")
async def admin_set_cookie_handler(callback: CallbackQuery, state: FSMContext):
    if str(callback.from_user.id) != ADMIN_ID:
        return

    await state.set_state(YTAuthState.waiting_cookie)

    await callback.message.answer(
        "🍪 Отправь новый Cookie.\n\n"
        "Сообщение будет сохранено в yt_auth.json",
        reply_markup=back_to_menu_keyboard
    )

    await callback.answer()

@router.message(YTAuthState.waiting_cookie)
async def admin_cookie_input_handler(message: Message, state: FSMContext):
    if str(message.from_user.id) != ADMIN_ID:
        return

    cookie_value = message.text.strip()

    if not cookie_value:
        await message.answer("Cookie не может быть пустым.")
        return

    set_yt_auth_value("Cookie", cookie_value)
    await state.clear()

    await message.answer("✅ Cookie обновлён.")

@router.callback_query(F.data == "admin_set_authorization")
async def admin_set_authorization_handler(callback: CallbackQuery, state: FSMContext):
    if str(callback.from_user.id) != ADMIN_ID:
        return

    await state.set_state(YTAuthState.waiting_authorization)

    await callback.message.answer(
        "🔑 Отправь новое значение Authorization.\n\n"
        "Сообщение будет сохранено в yt_auth.json",
        reply_markup=back_to_menu_keyboard
    )

    await callback.answer()

@router.message(YTAuthState.waiting_authorization)
async def admin_authorization_input_handler(message: Message, state: FSMContext):
    if str(message.from_user.id) != ADMIN_ID:
        return

    authorization_value = message.text.strip()

    if not authorization_value:
        await message.answer("Authorization не может быть пустым.")
        return

    set_yt_auth_value("authorization", authorization_value)
    await state.clear()

    await message.answer("✅ Authorization обновлён.")

@router.callback_query(F.data == "admin_set_user_agent")
async def admin_set_user_agent_handler(callback: CallbackQuery, state: FSMContext):
    if str(callback.from_user.id) != ADMIN_ID:
        return

    await state.set_state(YTAuthState.waiting_user_agent)

    await callback.message.answer(
        "🖥 Отправь новый User-Agent.\n\n"
        "Сообщение будет сохранено в yt_auth.json",
        reply_markup=back_to_menu_keyboard
    )

    await callback.answer()

@router.message(YTAuthState.waiting_user_agent)
async def admin_user_agent_input_handler(message: Message, state: FSMContext):
    if str(message.from_user.id) != ADMIN_ID:
        return

    user_agent_value = message.text.strip()

    if not user_agent_value:
        await message.answer("User-Agent не может быть пустым.")
        return

    set_yt_auth_value("User-Agent", user_agent_value)
    await state.clear()

    await message.answer("✅ User-Agent обновлён.")