import random

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from config import ADMIN_ID
from keyboards.main_keyboard import main_keyboard
from services.settings_service import get_setting
from youtube_music import ym_client

router = Router()


@router.message(Command("rand"))
async def random_track_command_handler(message: Message):
    if str(message.from_user.id) != ADMIN_ID:
        await message.answer("Это закрытая функция пользователя skibs505")
        return

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
            disable_web_page_preview=True,
        )

    except Exception as e:
        await message.answer(f"Ошибка: {e}")


@router.message(Command("playlist"))
async def random_liked_playlist_command_handler(message: Message):
    if str(message.from_user.id) != ADMIN_ID:
        await message.answer("Это закрытая функция пользователя skibs505")
        return

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

        await message.answer(
            f"🎶 <b>Случайный плейлист</b>\n"
            f"из понравившихся <b>{owner}</b>\n\n{text}",
            parse_mode="HTML",
            reply_markup=main_keyboard,
            disable_web_page_preview=True,
        )

    except Exception as e:
        await message.answer(f"Ошибка: {e}")


@router.callback_query(F.data == "random_liked_track")
async def random_liked_track_callback_handler(callback: CallbackQuery):
    if str(callback.from_user.id) != ADMIN_ID:
        await callback.answer("Это закрытая функция пользователя skibs505", show_alert=True)
        return

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
        owner = get_setting("owner")

        try:
            await callback.message.delete()
        except Exception:
            pass

        await callback.message.answer(
            f"🎲 <b>Случайный трек</b>\n"
            f"из понравившихся <b>{owner}</b>\n\n"
            f"🎵 <b>{artist}</b> — <a href='{url}'>{title}</a>",
            reply_markup=main_keyboard,
            parse_mode="HTML",
            disable_web_page_preview=True,
        )

    except Exception as e:
        await callback.message.answer(f"Ошибка: {e}")

    await callback.answer()


@router.callback_query(F.data == "random_liked_playlist")
async def random_liked_playlist_callback_handler(callback: CallbackQuery):
    if str(callback.from_user.id) != ADMIN_ID:
        await callback.answer("Это закрытая функция пользователя skibs505", show_alert=True)
        return

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

        try:
            await callback.message.delete()
        except Exception:
            pass

        await callback.message.answer(
            f"🎶 <b>Случайный плейлист</b>\n"
            f"из понравившихся <b>{owner}</b>\n\n{text}",
            parse_mode="HTML",
            reply_markup=main_keyboard,
            disable_web_page_preview=True,
        )

    except Exception as e:
        await callback.message.answer(f"Ошибка: {e}")

    await callback.answer()
