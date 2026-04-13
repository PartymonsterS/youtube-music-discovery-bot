import random

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from youtube_music import ym_client
from states.community_playlists import CommunityPlaylistState
from keyboards.community_playlists_keyboard import community_playlists_keyboard
from keyboards.main_keyboard import main_keyboard

router = Router()


@router.callback_query(F.data == "playlist_discovery")
async def start_playlist_discovery(callback: CallbackQuery, state: FSMContext):
    await state.set_state(CommunityPlaylistState.waiting_query)

    await callback.message.answer(
        "📚 <b>Playlist Discovery</b>\n\n"
        "Напиши жанр, тег или настроение.\n\n"
        "Примеры:\n"
        "• sad piano\n"
        "• gym phonk\n"
        "• jazz night",
        parse_mode="HTML"
    )

    await callback.answer()


@router.message(CommunityPlaylistState.waiting_query)
async def handle_playlist_query(message: Message, state: FSMContext):
    query = message.text.strip()

    ym_client.connect()
    playlists = ym_client.search_community_playlists(query, limit=30)

    if not playlists:
        await message.answer("Ничего не найдено.")
        await state.clear()
        return

    first = random.choice(playlists)

    await state.update_data(
        playlists=playlists,
        used_ids=[first["playlistId"]],
        query=query
    )

    await message.answer(
        f"📚 <b>Community Playlist</b>\n\n"
        f"🎵 <b>{first['title']}</b>\n"
        f"👤 {first['author']}\n"
        f"📦 {first['count']} tracks\n\n"
        f"<a href='{first['url']}'>Открыть</a>",
        parse_mode="HTML",
        reply_markup=community_playlists_keyboard()
    )


@router.callback_query(F.data == "community_playlist_next")
async def next_playlist(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    playlists = data.get("playlists", [])
    used_ids = data.get("used_ids", [])

    available = [
        p for p in playlists
        if p["playlistId"] not in used_ids
    ]

    if not available:
        await callback.message.answer("Плейлисты закончились.", reply_markup=main_keyboard)
        await state.clear()
        await callback.answer()
        return

    next_p = random.choice(available)
    used_ids.append(next_p["playlistId"])

    await state.update_data(used_ids=used_ids)

    await callback.message.delete()

    await callback.message.answer(
        f"📚 <b>Community Playlist</b>\n\n"
        f"🎵 <b>{next_p['title']}</b>\n"
        f"👤 {next_p['author']}\n"
        f"📦 {next_p['count']} tracks\n\n"
        f"<a href='{next_p['url']}'>Открыть</a>",
        parse_mode="HTML",
        reply_markup=community_playlists_keyboard()
    )

    await callback.answer()