from aiogram.fsm.state import StatesGroup, State

from aiogram.fsm.state import StatesGroup, State


class YTAuthState(StatesGroup):
    waiting_authorization = State()
    waiting_cookie = State()
    waiting_user_agent = State()
    waiting_auth_user = State()