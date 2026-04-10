import random

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from keyboards.main_keyboard import main_keyboard
from keyboards.back_to_menu_keyboard import back_to_menu_keyboard
from states.genre_playlist import SearchMusicState
from youtube_music import ym_client
from services.settings_service import get_setting

router = Router()


@router.callback_query(F.data == "playlist_search")
async def playlist_search_callback_handler(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.set_state(SearchMusicState.waiting_query)

    await callback.message.answer(
        "🎼 <b>Создание плейлиста</b>\n\n"
        "Напиши жанр, тег, исполнителя или описание музыки.\n\n"
        "Например:\n"
        "• phonk\n"
        "• funky jazz\n"
        "• sad piano\n"
        "• nightcore\n"
        "• Arctic Monkeys\n"
        "• aggressive gym music",
        parse_mode="HTML",
        reply_markup=back_to_menu_keyboard
    )

    await callback.answer()


@router.message(SearchMusicState.waiting_query)
async def playlist_query_handler(message: Message, state: FSMContext):
    query = message.text.strip()

    if not query:
        await message.answer("Запрос пустой. Напиши жанр, тег или артиста.")
        return

    await state.update_data(query=query)
    await state.set_state(SearchMusicState.waiting_count)

    await message.answer(
        "Сколько треков показать?\n"
        "Можно от 1 до 30."
    )


@router.message(SearchMusicState.waiting_count)
async def playlist_count_handler(message: Message, state: FSMContext):
    text = message.text.strip()

    if not text.isdigit():
        await message.answer("Введи число.")
        return

    count = int(text)

    max_count = get_setting("playlist_search_max_count")

    if count < 1 or count > max_count:
        await message.answer(
            f"Можно показать от 1 до {max_count} треков.",
            reply_markup=main_keyboard
        )
        return

    data = await state.get_data()
    query = data["query"]

    ym_client.connect()
    found_tracks = ym_client.search_tracks(query=query, limit=count * 5)

    if not found_tracks:
        await message.answer("Ничего не найдено.")
        await state.clear()
        return

    random_tracks = random.sample(found_tracks, min(count, len(found_tracks)))
    lines = []

    for i, track in enumerate(random_tracks, start=1):
        lines.append(
            f"{i}. 🎵 <b>{track['artist']}</b> — "
            f"<a href='{track['url']}'>{track['title']}</a>"
        )

    text = "\n\n".join(lines)

    await message.answer(
        f'🎼 <b>Результаты по запросу:</b> "{query}"\n\n{text}',
        parse_mode="HTML",
        reply_markup=main_keyboard,
        disable_web_page_preview=True
    )

    await state.clear()