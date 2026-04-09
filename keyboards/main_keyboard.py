from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


main_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➡️ Next", callback_data="next_track"),
        ],
        [
            InlineKeyboardButton(text="🎲 Random Playlist", callback_data="playlist"),
            InlineKeyboardButton(text="🎼 Genre Playlist", callback_data="genre_playlist"),
        ],
        [
            InlineKeyboardButton(text="ℹ️ Help", callback_data="help"),
        ]
    ]
)