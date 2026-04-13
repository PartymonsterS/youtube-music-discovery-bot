from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def community_playlists_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➡️ Next Playlist",
                    callback_data="community_playlist_next"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Back to menu",
                    callback_data="back_to_menu"
                )
            ]
        ]
    )