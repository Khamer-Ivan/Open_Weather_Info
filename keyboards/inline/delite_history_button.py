from telebot import types
from telebot.types import CallbackQuery

from loader import bot
from states.user_states import UserInfoState


def delete_day(call: CallbackQuery):
    """
    Функция, предоставляющая в виде inline кнопок выбор
    для удаления истории запросов за день.
    :param call: CallbackQuery
    :return: None
    """
    with bot.retrieve_data(call.message.chat.id) as data:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        delete_day_menu = types.InlineKeyboardMarkup(row_width=1)
        delete_button = types.InlineKeyboardButton(
                                                    text=data['language']['delete_day'],
                                                    callback_data='delete_day'
                                                    )
        user_history = types.InlineKeyboardButton(
                                                    text=data['language']['back_menu'],
                                                    callback_data='menu'
                                                    )
        delete_day_menu.add(delete_button, user_history)
        bot.send_message(
                            call.message.chat.id, data['language']['choose_command'],
                            reply_markup=delete_day_menu
                            )


def delete_week(call: CallbackQuery):
    """
    Функция, предоставляющая в виде inline кнопок выбор
    для удаления истории запросов за неделю.
    :param call: CallbackQuery
    :return: None
    """
    with bot.retrieve_data(call.message.chat.id) as data:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        delete_week_menu = types.InlineKeyboardMarkup(row_width=1)
        delete_button = types.InlineKeyboardButton(
                                                    text=data['language']['delete_week'],
                                                    callback_data='delete_week'
                                                    )
        user_history = types.InlineKeyboardButton(
                                                    text=data['language']['back_menu'],
                                                    callback_data='menu'
                                                    )
        delete_week_menu.add(delete_button, user_history)
        bot.send_message(
                            call.message.chat.id, data['language']['choose_command'],
                            reply_markup=delete_week_menu
                            )


def delete_all(call: CallbackQuery):
    """
    Функция, предоставляющая в виде inline кнопок выбор
    для удаления всей истории запросов.
    :param call: CallbackQuery
    :return: None
    """
    with bot.retrieve_data(call.message.chat.id) as data:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        delete_all_menu = types.InlineKeyboardMarkup(row_width=1)
        delete_button = types.InlineKeyboardButton(
                                                    text=data['language']['delete_all'],
                                                    callback_data='delete_all'
                                                    )
        user_history = types.InlineKeyboardButton(
                                                    text=data['language']['back_menu'],
                                                    callback_data='menu'
                                                    )
        delete_all_menu.add(delete_button, user_history)
        bot.send_message(
                            call.message.chat.id, data['language']['choose_command'],
                            reply_markup=delete_all_menu
                            )
