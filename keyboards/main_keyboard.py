from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🎲 Random Track",
                callback_data="random_liked_track"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🎲 Random Playlist",
                callback_data="random_liked_playlist"
            ),
            InlineKeyboardButton(
                text="🔎 Search Playlist",
                callback_data="playlist_search"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🎧 Music Flow",
                callback_data="music_flow"
            ),
        ],
        [
            InlineKeyboardButton(
                text="ℹ️ Help",
                callback_data="help"
            ),
        ]
    ]
)