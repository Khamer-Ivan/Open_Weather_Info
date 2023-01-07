from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    flag_day = 0
    flag_5_day = 0
    language = ''
