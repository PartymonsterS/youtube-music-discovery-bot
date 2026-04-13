from aiogram.fsm.state import StatesGroup, State


class CommunityPlaylistState(StatesGroup):
    waiting_query = State()