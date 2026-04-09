from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет.\n"
        "Это бот для анализа YouTube Music."
    )


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Команды:\n"
        "/start\n"
        "/help"
    )