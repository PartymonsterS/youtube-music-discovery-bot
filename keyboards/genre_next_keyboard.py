from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def genre_next_keyboard(query: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"➡️ Next: {query}",
                    callback_data="next_genre_track"
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

