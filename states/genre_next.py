from aiogram.fsm.state import StatesGroup, State


class GenreNextState(StatesGroup):
    waiting_query = State()