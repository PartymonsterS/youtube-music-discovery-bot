from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.main_keyboard import main_keyboard

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Привет 🎵\n\n"
        "Я бот для поиска и открытия музыки из YouTube Music.\n\n"
        "Я умею:\n"
        "• показывать случайные треки из библиотеки skibs505\n"
        "• создавать случайные плейлисты из понравившихся\n"
        "• создавать плейлисты по жанру, тегу или исполнителю\n"
        "• листать музыку как бесконечный поток (Music Flow)\n\n"
        "Выбери действие кнопкой ниже.",
        reply_markup=main_keyboard
    )
    await message.answer(f"Твой ID: {message.from_user.id}")


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu_callback_handler(callback: CallbackQuery, state: FSMContext):

    await state.clear()

    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer(
        "Привет 🎵\n\n"
        "Я бот для поиска и открытия музыки из YouTube Music.\n\n"
        "Я умею:\n"
        "• показывать случайные треки из библиотеки skibs505\n"
        "• создавать случайные плейлисты из понравившихся\n"
        "• создавать плейлисты по жанру, тегу или исполнителю\n"
        "• листать музыку как бесконечный поток (Music Flow)\n\n"
        "Выбери действие кнопкой ниже.",
        reply_markup=main_keyboard
    )

    await callback.answer()