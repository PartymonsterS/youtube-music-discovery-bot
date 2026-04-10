import random

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from keyboards.genre_next_keyboard import genre_next_keyboard
from keyboards.main_keyboard import main_keyboard
from keyboards.back_to_menu_keyboard import back_to_menu_keyboard
from states.genre_next import GenreNextState
from youtube_music import ym_client

router = Router()


@router.callback_query(F.data == "music_flow")
async def music_flow_callback_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GenreNextState.waiting_query)

    await callback.message.answer(
        "🎧 <b>Music Flow</b>\n\n"
        "Напиши, что хочешь послушать.\n\n"
        "Можно указать:\n"
        "• жанр\n"
        "• тег\n"
        "• исполнителя\n"
        "• настроение\n\n"
        "<i>Примеры:</i>\n"
        "phonk\n"
        "funky jazz\n"
        "Arctic Monkeys\n"
        "sad piano\n"
        "gym music\n\n"
        "➡️ После этого листай музыку кнопкой <b>Next</b>",
        parse_mode="HTML",
        reply_markup=back_to_menu_keyboard,

    )

    await callback.answer()


@router.message(GenreNextState.waiting_query)
async def music_flow_query_handler(message: Message, state: FSMContext):
    query = message.text.strip()

    if not query:
        await message.answer("Напиши жанр или тег.")
        return

    ym_client.connect()
    tracks = ym_client.search_tracks(query=query, limit=50)

    if not tracks:
        await message.answer("Ничего не найдено.")
        await state.clear()
        return

    first_track = random.choice(tracks)
    used_video_ids = [first_track["videoId"]]

    await state.update_data(
        genre_query=query,
        genre_tracks=tracks,
        used_video_ids=used_video_ids
    )

    await message.answer(
        f"🎧 <b>Music Flow:</b> {query}\n\n"
        f"🎵 <b>{first_track['artist']}</b> — "
        f"<a href='{first_track['url']}'>{first_track['title']}</a>",
        parse_mode="HTML",
        reply_markup=genre_next_keyboard(query)
    )


@router.callback_query(F.data == "music_flow_next")
async def music_flow_next_track_callback_handler(
    callback: CallbackQuery,
    state: FSMContext
):
    data = await state.get_data()

    query = data.get("genre_query")
    tracks = data.get("genre_tracks", [])
    used_video_ids = data.get("used_video_ids", [])

    if not query or not tracks:
        await callback.answer("Сессия закончилась. Начни заново.", show_alert=True)
        return

    available_tracks = [
        track for track in tracks
        if track["videoId"] not in used_video_ids
    ]

    if not available_tracks:
        await callback.message.delete()

        await callback.message.answer(
            f"🎧 <b>Music Flow:</b> {query}\n\n"
            "Треки по этому запросу закончились.",
            parse_mode="HTML",
            reply_markup=main_keyboard
        )

        await state.clear()
        await callback.answer()
        return

    next_track = random.choice(available_tracks)
    used_video_ids.append(next_track["videoId"])

    await state.update_data(used_video_ids=used_video_ids)

    await callback.message.delete()

    await callback.message.answer(
        f"🎧 <b>Music Flow:</b> {query}\n\n"
        f"🎵 <b>{next_track['artist']}</b> — "
        f"<a href='{next_track['url']}'>{next_track['title']}</a>",
        parse_mode="HTML",
        reply_markup=genre_next_keyboard(query)
    )

    await callback.answer()


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu_callback_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.delete()

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