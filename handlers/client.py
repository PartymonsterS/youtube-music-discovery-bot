import asyncio

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from youtube_music import ym_client

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
        "/sync"
        "/random"
    )

@router.message(Command("sync"))
async def sync_command(message: Message):
    ym_client.connect()
    ym_client.sync_tracks()
    count = ym_client.get_tracks_count()

    await message.answer("Треки были синхронизиорованы.")
    await message.answer(f"В твоих понравившихся {count} треков.")

@router.message(Command("random"))
async def random_command(message: Message):
    random_track = ym_client.get_liked_random_song()
    url = f"https://www.youtube.com/watch?v={random_track['videoId']}"

    await message.answer(f"**Ваш трек:** {url}")

