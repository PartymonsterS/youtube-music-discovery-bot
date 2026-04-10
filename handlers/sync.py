from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.main_keyboard import main_keyboard
from youtube_music import ym_client

from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()


@router.message(Command("sync"))
async def sync_handler(message: Message):
    await message.answer("⏳ Секунду, подождите... Синхронизирую библиотеку 🎧")

    try:
        ym_client.connect()
        result = ym_client.full_sync()

        await message.answer(
            "Синхронизация завершена ✅\n\n"
            f"В библиотеке найдено:\n"
            f"🎵 {result['total']} треков",
            reply_markup=main_keyboard
        )

    except Exception as e:
        await message.answer(f"Ошибка: {e}")


@router.message(Command("sync_new"))
async def sync_new_handler(message: Message):
    await message.answer("⏳ Секунду, подождите... Проверяю новые треки 🎧")

    try:
        ym_client.connect()
        result = ym_client.sync_new()

        await message.answer(
            "Обновление завершено ✅\n\n"
            f"Добавлено новых треков: {result['added']}\n"
            f"Всего треков: {result['total']}",
            reply_markup=main_keyboard
        )

    except Exception as e:
        await message.answer(f"Ошибка: {e}")


@router.callback_query(F.data == "sync")
async def sync_callback_handler(callback: CallbackQuery):
    await callback.message.answer(
        "⏳ Секунду, подождите... Синхронизирую библиотеку 🎧"
    )

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


@router.callback_query(F.data == "sync_new")
async def sync_new_callback_handler(callback: CallbackQuery):
    await callback.message.answer(
        "⏳ Секунду, подождите... Проверяю новые треки 🎧"
    )

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