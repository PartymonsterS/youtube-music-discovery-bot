from aiogram.fsm.state import StatesGroup, State

class SearchMusicState(StatesGroup):
    waiting_query = State()
    waiting_count = State()
