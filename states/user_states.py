from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    """
    Класс для хранения состояний пользователя
    """
    user_id = State()
    user_call = State()
    user_full_name = State()
    flag_day = State()
    flag_5_day = State()
    language = State()
    language_code = State()
