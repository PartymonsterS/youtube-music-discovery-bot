from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import ADMIN_ID

router = Router()


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "Админ панель\n"
        "Скоро здесь будут команды sync."
    )