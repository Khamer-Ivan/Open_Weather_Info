from telebot import types
from telebot.types import Message

from loader import bot
from states.user_states import UserInfoState


def delete_day(message: Message):
    delete_day_menu = types.InlineKeyboardMarkup(row_width=1)
    delete_button = types.InlineKeyboardButton(
                                                text=UserInfoState.language['delete_day'],
                                                callback_data='delete_day'
                                                )
    user_history = types.InlineKeyboardButton(
                                                text=UserInfoState.language['back_menu'],
                                                callback_data='menu'
                                                )
    delete_day_menu.add(delete_button, user_history)
    bot.send_message(
                        message.from_user.id, UserInfoState.language['choose_command'],
                        reply_markup=delete_day_menu
                        )


def delete_week(message: Message):
    delete_week_menu = types.InlineKeyboardMarkup(row_width=1)
    delete_button = types.InlineKeyboardButton(
                                                text=UserInfoState.language['delete_week'],
                                                callback_data='delete_week'
                                                )
    user_history = types.InlineKeyboardButton(
                                                text=UserInfoState.language['back_menu'],
                                                callback_data='menu'
                                                )
    delete_week_menu.add(delete_button, user_history)
    bot.send_message(
                        message.from_user.id, message.from_user.id, UserInfoState.language['choose_command'],
                        reply_markup=delete_week_menu
                        )


def delete_all(message: Message):
    delete_all_menu = types.InlineKeyboardMarkup(row_width=1)
    delete_button = types.InlineKeyboardButton(
                                                text=UserInfoState.language['delete_all'],
                                                callback_data='delete_all'
                                                )
    user_history = types.InlineKeyboardButton(
                                                text=UserInfoState.language['back_menu'],
                                                callback_data='menu'
                                                )
    delete_all_menu.add(delete_button, user_history)
    bot.send_message(
                        message.from_user.id, message.from_user.id, UserInfoState.language['choose_command'],
                        reply_markup=delete_all_menu
                        )
