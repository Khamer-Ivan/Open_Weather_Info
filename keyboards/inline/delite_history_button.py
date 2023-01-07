from telebot import types
from telebot.types import Message

from loader import bot
from states.user_states import UserInfoState
from translation import translator as tr


def delete_day(message: Message):
    delete_day_menu = types.InlineKeyboardMarkup(row_width=1)
    delete_button = types.InlineKeyboardButton(
                                                text=tr('Удалить историю за день', 'ru', UserInfoState.language),
                                                callback_data='delete_day'
                                                )
    user_history = types.InlineKeyboardButton(
                                                text=tr('Возврат в основное меню', 'ru', UserInfoState.language),
                                                callback_data='menu'
                                                )
    delete_day_menu.add(delete_button, user_history)
    bot.send_message(
                        message.from_user.id,
                        tr('Пожалуйста, выберите команду.', 'ru', UserInfoState.language),
                        reply_markup=delete_day_menu
                        )


def delete_week(message: Message):
    delete_week_menu = types.InlineKeyboardMarkup(row_width=1)
    delete_button = types.InlineKeyboardButton(
                                                text=tr('Удалить историю за неделю', 'ru', UserInfoState.language),
                                                callback_data='delete_week'
                                                )
    user_history = types.InlineKeyboardButton(
                                                text=tr('Возврат в основное меню', 'ru', UserInfoState.language),
                                                callback_data='menu'
                                                )
    delete_week_menu.add(delete_button, user_history)
    bot.send_message(
                        message.from_user.id,
                        tr('Пожалуйста, выберите команду.', 'ru', UserInfoState.language),
                        reply_markup=delete_week_menu
                        )


def delete_all(message: Message):
    delete_all_menu = types.InlineKeyboardMarkup(row_width=1)
    delete_button = types.InlineKeyboardButton(
                                                text=tr('Удалить историю запросов', 'ru', UserInfoState.language),
                                                callback_data='delete_all'
                                                )
    user_history = types.InlineKeyboardButton(
                                                text=tr('Возврат в основное меню', 'ru', UserInfoState.language),
                                                callback_data='menu'
                                                )
    delete_all_menu.add(delete_button, user_history)
    bot.send_message(
                        message.from_user.id,
                        tr('Пожалуйста, выберите команду.', 'ru', UserInfoState.language),
                        reply_markup=delete_all_menu
                        )
