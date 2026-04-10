from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


def genre_next_keyboard(query: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"➡️ Next: {query}",
                    callback_data="music_flow_next"
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

