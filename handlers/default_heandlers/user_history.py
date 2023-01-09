import timedelta
from telebot import types
from telebot.types import Message
from datetime import datetime

from loader import bot
from handlers.default_heandlers.start import Weather
from keyboards.inline import delite_history_button
from handlers.default_heandlers.start import bot_start
from states.user_states import UserInfoState


@bot.callback_query_handler(func=lambda call: call.data.endswith('user_history'))
def weather_button(message: Message) -> None:
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
                        message.from_user.id,
                        UserInfoState.language['choose_history'],
                        reply_markup=start_menu
                        )


@bot.callback_query_handler(func=lambda call: call.data.endswith('for_day'))
def history_for_day(message: Message) -> None:
    text = UserInfoState.language['history_day']
    for history in Weather.select().where(
            (Weather.user_id == message.from_user.id)
            & (Weather.date.startswith(datetime.now().strftime("%Y-%m-%d")))):
        text += f'\n{history.name}\n{history.request}\n{history.date}\n'
    if len(text) > 26:
        bot.send_message(message.from_user.id, text)
        delite_history_button.delete_day(message)
    else:
        bot.send_message(message.from_user.id, UserInfoState.language['history_empty'])
        bot_start(message)


@bot.callback_query_handler(func=lambda call: call.data.endswith('for_week'))
def history_for_week(message: Message) -> None:
    date_days_before = datetime.now() - timedelta.Timedelta(days=7)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    week_ago = date_days_before.strftime("%Y-%m-%d %H:%M:%S")
    text = UserInfoState.language['history_week']
    for history in Weather.select().where(
            (Weather.user_id == message.from_user.id)
            & (Weather.date.between(week_ago, now))):
        text += f'\n{history.name}\n{history.request}\n{history.date}\n'
    if len(text) > 28:
        bot.send_message(message.from_user.id, text)
        delite_history_button.delete_day(message)
    else:
        bot.send_message(message.from_user.id, UserInfoState.language['history_empty'])
        bot_start(message)


@bot.callback_query_handler(func=lambda call: call.data.endswith('for_all'))
def history_for_all(message: Message) -> None:
    text = UserInfoState.language['history_all']
    for history in Weather.select().where(Weather.user_id == message.from_user.id):
        text += f'\n{history.name}\n{history.request}\n{history.date}\n'
    if len(text) > 31:
        bot.send_message(message.from_user.id, text)
        delite_history_button.delete_day(message)
    else:
        bot.send_message(message.from_user.id, UserInfoState.language['history_empty'])
        bot_start(message)
