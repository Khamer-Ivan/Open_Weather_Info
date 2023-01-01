from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    day = State()
    week = State()
