from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from config import ADMIN_ID
from keyboards.main_keyboard import main_keyboard

router = Router()


def build_help_text(user_id: int) -> str:
    if str(user_id) == ADMIN_ID:
        return (
            "ℹ️ <b>Помощь</b>\n\n"
            "<b>Команды:</b>\n"
            "/sync — синхронизировать понравившиеся треки\n"
            "/sync_new — добавить только новые треки\n"
            "/rand — случайный трек из лайкнутых\n"
            "/playlist — случайный плейлист из лайкнутых\n"
            "/help — список команд\n\n"
            "<b>Кнопки:</b>\n"
            "🎲 Random Track — случайный трек\n"
            "🎲 Random Playlist — случайный плейлист\n"
            "🔎 Search Playlist — плейлист по запросу\n"
            "🎧 Music Flow — листать музыку"
        )

    return (
        "ℹ️ <b>Помощь</b>\n\n"
        "<b>Команды:</b>\n"
        "/help — список команд\n\n"
        "<b>Кнопки:</b>\n"
        "🔎 Search Playlist — плейлист по запросу\n"
        "🎧 Music Flow — листать музыку"
    )


@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(
        build_help_text(message.from_user.id),
        reply_markup=main_keyboard,
        parse_mode="HTML"
    )


@router.callback_query(F.data == "help")
async def help_callback_handler(callback: CallbackQuery):
    await callback.message.answer(
        build_help_text(callback.from_user.id),
        reply_markup=main_keyboard,
        parse_mode="HTML"
    )
    await callback.answer()