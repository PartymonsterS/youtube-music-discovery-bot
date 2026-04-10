from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.main_keyboard import main_keyboard
from keyboards.back_to_menu_keyboard import back_to_menu_keyboard
from youtube_music import ym_client
import random
from services.settings_service import get_setting


router = Router()


@router.message(Command("rand"))
async def random_track_command_handler(message: Message):
    try:
        random_track = ym_client.get_liked_random()

        title = random_track.get("title", "Unknown title")
        artist = (
            random_track["artists"][0]["name"]
            if random_track.get("artists")
            else "Unknown artist"
        )
        video_id = random_track.get("videoId")

        if not video_id:
            await message.answer(f"🎵 {artist} — {title}\nСсылка не найдена")
            return

        url = f"https://music.youtube.com/watch?v={video_id}"

        owner = get_setting("owner")
        await message.answer(
            f"🎲 <b>Случайный трек</b>\n"
            f"из понравившихся <b>{owner}</b>\n\n"
            f"🎵 <b>{artist}</b> — <a href='{url}'>{title}</a>",
            reply_markup=main_keyboard,
            parse_mode="HTML",
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

        playlist_size = get_setting("random_playlist_size")
        random_tracks = random.sample(tracks, min(playlist_size, len(tracks)))

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

        owner = get_setting("owner")
        await message.answer(
            f"🎶 <b>Случайный плейлист</b>\n"
            f"из понравившихся <b>{owner}</b>\n\n{text}",
            parse_mode="HTML",
            reply_markup=main_keyboard,
            disable_web_page_preview=True
        )

    except Exception as e:
        await message.answer(f"Ошибка: {e}")


@router.callback_query(F.data == "random_liked_track")
async def random_track_callback_handler(callback: CallbackQuery):
    try:
        random_track = ym_client.get_liked_random()

        title = random_track.get("title", "Unknown title")
        artist = (
            random_track["artists"][0]["name"]
            if random_track.get("artists")
            else "Unknown artist"
        )
        video_id = random_track.get("videoId")

        if not video_id:
            await callback.message.answer(f"🎵 {artist} — {title}\nСсылка не найдена")
            await callback.answer()
            return

        url = f"https://music.youtube.com/watch?v={video_id}"

        owner = get_setting("owner")
        await callback.message.answer(
            f"🎲 <b>Случайный трек</b>\n"
            f"из понравившихся <b>owner</b>\n\n"
            f"🎵 <b>{artist}</b> — <a href='{url}'>{title}</a>",
            reply_markup=main_keyboard,
            parse_mode="HTML",
        )

    except Exception as e:
        await callback.message.answer(f"Ошибка: {e}")

    await callback.answer()



@router.callback_query(F.data == "random_liked_playlist")
async def random_liked_playlist_callback_handler(callback: CallbackQuery):
    try:
        tracks = ym_client.get_liked_songs()

        if not tracks:
            await callback.message.answer("Нет треков. Сначала сделай /sync")
            await callback.answer()
            return

        playlist_size = get_setting("random_playlist_size")
        random_tracks = random.sample(tracks, min(playlist_size, len(tracks)))
        lines = []

        for i, track in enumerate(random_tracks, start=1):
            title = track.get("title", "Unknown title")
            artist = (
                track["artists"][0]["name"]
                if track.get("artists")
                else "Unknown artist"
            )
            video_id = track.get("videoId")

            if not video_id:
                continue

            url = f"https://music.youtube.com/watch?v={video_id}"

            lines.append(
                f"{i}. 🎵 <b>{artist}</b> — <a href='{url}'>{title}</a>"
            )

        text = "\n\n".join(lines)

        owner = get_setting("owner")
        await callback.message.answer(
            f"🎶 <b>Случайный плейлист</b>\n"
            f"из понравившихся <b>{owner}</b>\n\n{text}",
            parse_mode="HTML",
            reply_markup=main_keyboard,
            disable_web_page_preview=True
        )

    except Exception as e:
        await callback.message.answer(f"Ошибка: {e}")

    await callback.answer()


@router.callback_query(F.data == "random_track")
async def random_liked_track_callback_handler(callback: CallbackQuery):
    try:
        random_track = ym_client.get_liked_random()

        title = random_track.get("title", "Unknown title")
        artist = (
            random_track["artists"][0]["name"]
            if random_track.get("artists")
            else "Unknown artist"
        )
        video_id = random_track.get("videoId")

        if not video_id:
            await callback.answer("Ссылка не найдена", show_alert=True)
            return

        url = f"https://music.youtube.com/watch?v={video_id}"

        await callback.message.delete()

        owner = get_setting("owner")
        await callback.message.answer(
            f"🎲 <b>Случайный трек</b>\n"
            f"из понравившихся <b>{owner}</b>\n\n"
            f"🎵 <b>{artist}</b> — <a href='{url}'>{title}</a>",
            reply_markup=main_keyboard,
            parse_mode="HTML",
        )

        await callback.answer()

    except Exception as e:
        await callback.answer("Ошибка", show_alert=True)
        await callback.message.answer(f"Ошибка: {e}", reply_markup=back_to_menu_keyboard)