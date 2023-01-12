from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    """
    Класс для хранения состояний пользователя
    """
    user_id = 0
    user_call = ''
    user_full_name = ''
    flag_day = 0
    flag_5_day = 0
    language = {}
    language_code = ''
