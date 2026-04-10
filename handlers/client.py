import random
import html
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from youtube_music import ym_client
from keyboards.main_keyboard import main_keyboard

from aiogram.fsm.context import FSMContext
from states.genre_playlist import SearchMusicState

from states.genre_next import GenreNextState
from keyboards.genre_next_keyboard import genre_next_keyboard

router = Router()


def format_track_html(track: dict, index: int | None = None) -> str:
    title = track.get("title", "Unknown title")
    artist = track["artists"][0]["name"] if track.get("artists") else "Unknown artist"
    video_id = track.get("videoId")

    if video_id:
        line = f"🎵 <b>{artist}</b> — <a href='https://music.youtube.com/watch?v={video_id}'>{title}</a>"
    else:
        line = f"🎵 <b>{artist}</b> — {title}"

    if index is not None:
        return f"{index}. {line}"

    return line


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет 🎵\n\n"
        "Я бот для поиска и открытия музыки из YouTube Music.\n\n"
        "Я умею:\n"
        "• показывать случайные треки из твоей библиотеки\n"
        "• создавать случайные плейлисты\n"
        "• создавать плейлисты по жанру или тегу\n"
        "• листать треки по жанру как радио\n\n"
        "Выбери действие кнопкой ниже или напиши /help",
        reply_markup=main_keyboard
    )

@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Доступные команды:\n\n"
        "/sync — полная синхронизация понравившихся треков\n"
        "/sync_new — добавить только новые треки\n\n"
        "/rand — случайный трек из библиотеки\n"
        "/playlist — случайный плейлист (10 треков)\n\n"
        "/help — список команд",
        reply_markup=main_keyboard
    )


@router.message(Command("sync"))
async def sync_command(message: Message):
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
async def sync_new_command(message: Message):
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


@router.message(Command("rand"))
async def rand_command(message: Message):
    try:
        random_track = ym_client.get_liked_random()

        title = random_track.get("title", "Unknown title")
        artist = random_track["artists"][0]["name"] if random_track.get("artists") else "Unknown artist"
        video_id = random_track.get("videoId")

        if not video_id:
            await message.answer(f"🎵 {artist} — {title}\nСсылка не найдена")
            return

        url = f"https://music.youtube.com/watch?v={video_id}"

        await message.answer(
            f"🎲 <b>Твой случайный трек</b>\n\n"
            f"🎵 <b>{artist}</b> — <a href='{url}'>{title}</a>",
            reply_markup=main_keyboard,
            parse_mode="HTML"
        )

    except Exception as e:
        await message.answer(f"Ошибка: {e}")


@router.message(Command("playlist"))
async def command_playlist(message: Message):
    try:
        tracks = ym_client.get_liked_songs()

        if not tracks:
            await message.answer("Нет треков. Сначала сделай /sync")
            return

        random_tracks = random.sample(tracks, min(10, len(tracks)))
        lines = []

        for i, track in enumerate(random_tracks, start=1):
            title = track.get("title", "Unknown title")
            artist = track["artists"][0]["name"] if track.get("artists") else "Unknown artist"
            video_id = track.get("videoId")

            if not video_id:
                continue

            url = f"https://music.youtube.com/watch?v={video_id}"

            lines.append(
                f"{i}. 🎵 <b>{artist}</b> — "
                f"<a href='{url}'>{title}</a>"
            )

        text = "\n\n".join(lines)

        await message.answer(
            f"🎶 <b>Твой случайный плейлист</b>\n\n{text}",
            parse_mode="HTML",
            reply_markup=main_keyboard,
            disable_web_page_preview=True
        )

    except Exception as e:
        await message.answer(f"Ошибка: {e}")


@router.callback_query(F.data == "help")
async def help_callback(callback: CallbackQuery):
    await callback.message.answer(
        "Доступные команды:\n\n"
        "/sync — полная синхронизация понравившихся треков\n"
        "/sync_new — добавить только новые треки\n\n"
        "/rand — случайный трек из библиотеки\n"
        "/playlist — случайный плейлист (10 треков)\n\n"
        "/help — список команд",
        reply_markup=main_keyboard
    )
    await callback.answer()


@router.callback_query(F.data == "sync")
async def sync_callback(callback: CallbackQuery):
    await callback.message.answer("⏳ Секунду, подождите... Синхронизирую библиотеку 🎧")

    try:
        ym_client.connect()
        result = ym_client.full_sync()

        await callback.message.answer(
            "Синхронизация завершена ✅\n\n"
            f"В библиотеке найдено:\n"
            f"🎵 {result['total']} треков",
            reply_markup=main_keyboard
        )
    except Exception as e:
        await callback.message.answer(f"Ошибка: {e}")

    await callback.answer()


@router.callback_query(F.data == "sync_new")
async def sync_new_callback(callback: CallbackQuery):
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


@router.callback_query(F.data == "rand")
async def rand_callback(callback: CallbackQuery):
    try:
        random_track = ym_client.get_liked_random()

        title = random_track.get("title", "Unknown title")
        artist = random_track["artists"][0]["name"] if random_track.get("artists") else "Unknown artist"
        video_id = random_track.get("videoId")

        if not video_id:
            await callback.message.answer(f"🎵 {artist} — {title}\nСсылка не найдена")
            await callback.answer()
            return

        url = f"https://music.youtube.com/watch?v={video_id}"

        await callback.message.answer(
            f"🎲 <b>Случайный трек</b>\n\n"
            f"🎵 <b>{artist}</b> — <a href='{url}'>{title}</a>",
            reply_markup=main_keyboard,
            parse_mode="HTML",
            disable_web_page_preview=True
        )
    except Exception as e:
        await callback.message.answer(f"Ошибка: {e}")

    await callback.answer()


@router.callback_query(F.data == "playlist")
async def playlist_callback(callback: CallbackQuery):
    try:
        tracks = ym_client.get_liked_songs()

        if not tracks:
            await callback.message.answer("Нет треков. Сначала сделай /sync")
            await callback.answer()
            return

        random_tracks = random.sample(tracks, min(10, len(tracks)))
        lines = []

        for i, track in enumerate(random_tracks, start=1):
            title = track.get("title", "Unknown title")
            artist = track["artists"][0]["name"] if track.get("artists") else "Unknown artist"
            video_id = track.get("videoId")

            if not video_id:
                continue

            url = f"https://music.youtube.com/watch?v={video_id}"

            lines.append(
                f"{i}. 🎵 <b>{artist}</b> — <a href='{url}'>{title}</a>"
            )

        text = "\n\n".join(lines)

        await callback.message.answer(
            f"🎶 <b>Твой случайный плейлист</b>\n\n{text}",
            reply_markup=main_keyboard,
            parse_mode="HTML",
            disable_web_page_preview=True
        )

    except Exception as e:
        await callback.message.answer(f"Ошибка: {e}")

    await callback.answer()


@router.callback_query(F.data == "next_track")
async def next_track_callback(callback: CallbackQuery):
    try:
        random_track = ym_client.get_liked_random()

        title = random_track.get("title", "Unknown title")
        artist = random_track["artists"][0]["name"] if random_track.get("artists") else "Unknown artist"
        video_id = random_track.get("videoId")

        if not video_id:
            await callback.answer("Ссылка не найдена", show_alert=True)
            return

        url = f"https://music.youtube.com/watch?v={video_id}"

        await callback.message.delete()

        await callback.message.answer(
            f"🎲 <b>Случайный трек</b>\n\n"
            f"🎵 <b>{artist}</b> — <a href='{url}'>{title}</a>",
            reply_markup=main_keyboard,
            parse_mode="HTML"
        )

        await callback.answer()

    except Exception as e:
        await callback.answer("Ошибка", show_alert=True)
        await callback.message.answer(f"Ошибка: {e}")


@router.callback_query(F.data == "genre_playlist")
async def genre_playlist_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SearchMusicState.waiting_query)

    await callback.message.answer(
        "Напиши жанр или тег для поиска.\n\n"
        "Например:\n"
        "phonk\n"
        "jazz\n"
        "rock\n"
        "nightcore"
    )

    await callback.answer()


@router.message(SearchMusicState.waiting_query)
async def search_query_handler(message: Message, state: FSMContext):
    query = message.text.strip()

    if not query:
        await message.answer("Запрос пустой. Напиши жанр, тег или артиста.")
        return

    await state.update_data(query=query)
    await state.set_state(SearchMusicState.waiting_count)

    await message.answer(
        "Сколько треков показать?\n"
        "Например: 5, 10, 20"
    )


@router.message(SearchMusicState.waiting_count)
async def search_count_handler(message: Message, state: FSMContext):
    text = message.text.strip()

    if not text.isdigit():
        await message.answer("Введи число.")
        return

    count = int(text)

    data = await state.get_data()
    query = data["query"]

    ym_client.connect()

    found_tracks = ym_client.search_tracks(query=query, limit=50)

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


@router.callback_query(F.data == "genre_next")
async def genre_next_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GenreNextState.waiting_query)

    await callback.message.answer(
        "🎼 <b>Genre Next mode</b>\n\n"
        "Напиши жанр или тег.\n\n"
        "Например:\n"
        "phonk\n"
        "jazz\n"
        "rock\n"
        "nightcore",
        parse_mode="HTML"
    )

    await callback.answer()

@router.message(GenreNextState.waiting_query)
async def genre_next_query_handler(message: Message, state: FSMContext):
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
        f"🎼 <b>Genre Next:</b> {query}\n\n"
        f"🎵 <b>{first_track['artist']}</b> — "
        f"<a href='{first_track['url']}'>{first_track['title']}</a>",
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=genre_next_keyboard(query)
    )

@router.callback_query(F.data == "next_genre_track")
async def next_genre_track_callback(callback: CallbackQuery, state: FSMContext):
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
            f"🎼 <b>Genre Next:</b> {query}\n\n"
            "Треки по этому тегу закончились.",
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
        f"🎼 <b>Genre Next:</b> {query}\n\n"
        f"🎵 <b>{next_track['artist']}</b> — "
        f"<a href='{next_track['url']}'>{next_track['title']}</a>",
        parse_mode="HTML",
        reply_markup=genre_next_keyboard(query)
    )

    await callback.answer()

@router.callback_query(F.data == "back_to_menu")
async def back_to_menu_callback(callback: CallbackQuery, state: FSMContext):

    await state.clear()

    await callback.message.delete()

    await callback.message.answer(
        "Привет 🎵\n\n"
        "Я бот для анализа твоей библиотеки YouTube Music.\n\n"
        "Я умею:\n"
        "• синхронизировать понравившиеся треки\n"
        "• выбирать случайный трек\n"
        "• создавать случайный плейлист\n\n"
        "Выбери действие кнопкой ниже или напиши /help",
        reply_markup=main_keyboard
    )

    await callback.answer()
