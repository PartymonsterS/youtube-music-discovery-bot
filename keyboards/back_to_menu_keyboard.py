from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

back_to_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⬅️ Back to menu",
                callback_data="back_to_menu"
            )
        ]
    ]
)