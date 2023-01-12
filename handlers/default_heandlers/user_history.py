import timedelta
from telebot import types
from telebot.types import CallbackQuery
from datetime import datetime

from loader import bot
from handlers.default_heandlers.start import Weather
from keyboards.inline import delite_history_button
from handlers.default_heandlers.menu import main_menu
from states.user_states import UserInfoState
from utils.logging_setting import exception_handler


@bot.callback_query_handler(func=lambda call: call.data.endswith('user_history'))
@bot.message_handler(commands=['history'])
@exception_handler
def weather_button(call: CallbackQuery) -> None:
    """
    Функция, предоставляющая в виде inline кнопок выбор
    периода отображения запросов пользователя.
    :param call: CallbackQuery
    :return: None
    """
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    start_menu = types.InlineKeyboardMarkup(row_width=1)
    for_day = types.InlineKeyboardButton(
                                            text=UserInfoState.language['for_day'],
                                            callback_data='for_day'
                                            )
    for_week = types.InlineKeyboardButton(
                                            text=UserInfoState.language['for_week'],
                                            callback_data='for_week'
                                            )
    for_all = types.InlineKeyboardButton(
                                            text=UserInfoState.language['for_all'],
                                            callback_data='for_all')
    menu = types.InlineKeyboardButton(
                                            text=UserInfoState.language['back_menu'],
                                            callback_data='menu'
                                            )
    start_menu.add(for_day, for_week, for_all, menu)
    bot.send_message(
                        call.message.chat.id,
                        UserInfoState.language['choose_history'],
                        reply_markup=start_menu
                        )


@bot.callback_query_handler(func=lambda call: call.data.endswith('for_day'))
@exception_handler
def history_for_day(call: CallbackQuery) -> None:
    """
    Функция, предоставляющая историю запросов за один день.
    :param call: CallbackQuery
    :return: None
    """
    text = UserInfoState.language['history_day']
    for history in Weather.select().where(
            (Weather.user_id == UserInfoState.user_id)
            & (Weather.date.startswith(datetime.now().strftime("%Y-%m-%d")))):
        text += f'\n{history.name}\n{history.request}\n{history.date}\n'
    if len(text) > 26:
        bot.send_message(call.message.chat.id, text)
        delite_history_button.delete_day(call)
    else:
        bot.send_message(call.message.chat.id, UserInfoState.language['history_empty'])
        main_menu(call)


@bot.callback_query_handler(func=lambda call: call.data.endswith('for_week'))
@exception_handler
def history_for_week(call: CallbackQuery) -> None:
    """
    Функция, предоставляющая историю запросов за одну неделю.
    :param call: CallbackQuery
    :return: None
    """
    date_days_before = datetime.now() - timedelta.Timedelta(days=7)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    week_ago = date_days_before.strftime("%Y-%m-%d %H:%M:%S")
    text = UserInfoState.language['history_week']
    for history in Weather.select().where(
            (Weather.user_id == UserInfoState.user_id)
            & (Weather.date.between(week_ago, now))):
        text += f'\n{history.name}\n{history.request}\n{history.date}\n'
    if len(text) > 28:
        bot.send_message(call.message.chat.id, text)
        delite_history_button.delete_week(call)
    else:
        bot.send_message(call.message.chat.id, UserInfoState.language['history_empty'])
        main_menu(call)


@bot.callback_query_handler(func=lambda call: call.data.endswith('for_all'))
@exception_handler
def history_for_all(call: CallbackQuery) -> None:
    """
    Функция, предоставляющая всю историю запросов.
    :param call: CallbackQuery
    :return: None
    """
    text = UserInfoState.language['history_all']
    for history in Weather.select().where(Weather.user_id == UserInfoState.user_id):
        text += f'\n{history.name}\n{history.request}\n{history.date}\n'
    if len(text) > 31:
        bot.send_message(call.message.chat.id, text)
        delite_history_button.delete_all(call)
    else:
        bot.send_message(bot.message.chat.id, UserInfoState.language['history_empty'])
        main_menu(call)
