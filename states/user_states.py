from telebot.handler_backends import State, StatesGroup
from languages import russian


class UserInfoState(StatesGroup):
    user_id = 0
    user_full_name = ''
    flag_day = 0
    flag_5_day = 0
    language = {}
    language_code = ''
