import timedelta
from telebot import types
from telebot.types import Message
from datetime import datetime

from loader import bot
from handlers.default_heandlers.start import Weather
from keyboards.inline import delite_history_button
from handlers.default_heandlers.start import bot_start
from states.user_states import UserInfoState
from translation import translator as tr


@bot.callback_query_handler(func=lambda call: call.data.endswith('user_history'))
def weather_button(message: Message) -> None:
    start_menu = types.InlineKeyboardMarkup(row_width=1)
    for_day = types.InlineKeyboardButton(
                                            text=tr('За день', 'ru', UserInfoState.language),
                                            callback_data='for_day'
                                            )
    for_week = types.InlineKeyboardButton(
                                            text=tr('За неделю', 'ru', UserInfoState.language),
                                            callback_data='for_week'
                                            )
    for_all = types.InlineKeyboardButton(
                                            text=tr('За всё время', 'ru', UserInfoState.language),
                                            callback_data='for_all')
    menu = types.InlineKeyboardButton(
                                            text=tr('Возврат в основное меню', 'ru', UserInfoState.language),
                                            callback_data='menu'
                                            )
    start_menu.add(for_day, for_week, for_all, menu)
    bot.send_message(
                        message.from_user.id,
                        tr('Пожалуйста, выберите период отображения запросов.', 'ru', UserInfoState.language),
                        reply_markup=start_menu
                        )


@bot.callback_query_handler(func=lambda call: call.data.endswith('for_day'))
def history_for_day(message: Message) -> None:
    text = tr('История запросов за день:\n', 'ru', UserInfoState.language)
    for history in Weather.select().where(
            (Weather.user_id == message.from_user.id)
            & (Weather.date.startswith(datetime.now().strftime("%Y-%m-%d")))):
        text += f'\n{history.name}\n{history.request}\n{history.date}\n'
    if len(text) > 26:
        bot.send_message(message.from_user.id, text)
        delite_history_button.delete_day(message)
    else:
        bot.send_message(message.from_user.id, tr('История запросов пуста.', 'ru', UserInfoState.language))
        bot_start(message)


@bot.callback_query_handler(func=lambda call: call.data.endswith('for_week'))
def history_for_week(message: Message) -> None:
    date_days_before = datetime.now() - timedelta.Timedelta(days=7)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    week_ago = date_days_before.strftime("%Y-%m-%d %H:%M:%S")
    text = tr('История запросов за неделю:\n', 'ru', UserInfoState.language)
    for history in Weather.select().where(
            (Weather.user_id == message.from_user.id)
            & (Weather.date.between(week_ago, now))):
        text += f'\n{history.name}\n{history.request}\n{history.date}\n'
    if len(text) > 28:
        bot.send_message(message.from_user.id, text)
        delite_history_button.delete_day(message)
    else:
        bot.send_message(message.from_user.id, tr('История запросов пуста.', 'ru', UserInfoState.language))
        bot_start(message)


@bot.callback_query_handler(func=lambda call: call.data.endswith('for_all'))
def history_for_all(message: Message) -> None:
    text = tr('История запросов за всё время:\n', 'ru', UserInfoState.language)
    for history in Weather.select().where(Weather.user_id == message.from_user.id):
        text += f'\n{history.name}\n{history.request}\n{history.date}\n'
    if len(text) > 31:
        bot.send_message(message.from_user.id, text)
        delite_history_button.delete_day(message)
    else:
        bot.send_message(message.from_user.id, tr('История запросов пуста.', 'ru', UserInfoState.language))
        bot_start(message)
