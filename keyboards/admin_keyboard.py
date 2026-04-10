from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


admin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📊 Show settings",
                callback_data="admin_show_settings"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔄 Full sync",
                callback_data="admin_full_sync"
            ),
            InlineKeyboardButton(
                text="➕ Sync new",
                callback_data="admin_sync_new"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔑 Set Authorization",
                callback_data="admin_set_authorization"
            )
        ],
        [
            InlineKeyboardButton(
                text="🍪 Set Cookie",
                callback_data="admin_set_cookie"
            )
        ],
        [
            InlineKeyboardButton(
                text="🖥 Set User-Agent",
                callback_data="admin_set_user_agent"
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