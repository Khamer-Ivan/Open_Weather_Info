from datetime import datetime
from timedelta import Timedelta
from telebot.types import Message, CallbackQuery

from loader import bot
from handlers.default_heandlers.start import Weather
from handlers.default_heandlers.menu import main_menu
from states.user_states import UserInfoState


@bot.callback_query_handler(func=lambda call: call.data.endswith('delete_day'))
def delete_day(call: CallbackQuery) -> None:
    message_counter = 0
    for history in Weather.select().where(
            (Weather.user_id == UserInfoState.user_id)
            & (Weather.date.startswith(datetime.now().strftime("%Y-%m-%d")))):
        history.delete_instance()
        message_counter += 1
    bot.send_message(call.message.chat.id, f'{UserInfoState.language["delete_history"]}'
                                           f'{UserInfoState.language["delete_count"]} {message_counter}')
    main_menu(call)


@bot.callback_query_handler(func=lambda call: call.data.endswith('delete_week'))
def delete_week(call: CallbackQuery) -> None:
    message_counter = 0
    date_days_before = datetime.now() - Timedelta(days=7)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    week_ago = date_days_before.strftime("%Y-%m-%d %H:%M:%S")
    for history in Weather.select().where(
            (Weather.user_id == UserInfoState.user_id)
            & (Weather.date.between(week_ago, now))):
        history.delete_instance()
        message_counter += 1
    bot.send_message(call.message.chat.id, f'{UserInfoState.language["delete_history"]}'
                                           f'{UserInfoState.language["delete_count"]} {message_counter}')
    main_menu(call)


@bot.callback_query_handler(func=lambda call: call.data.endswith('delete_all'))
def delete_all(call: CallbackQuery) -> None:
    message_counter = 0
    for history in Weather.select().where(Weather.user_id == UserInfoState.user_id):
        history.delete_instance()
        message_counter += 1
    bot.send_message(call.message.chat.id, f'{UserInfoState.language["delete_history"]}'
                                           f'{UserInfoState.language["delete_count"]} {message_counter}')
    main_menu(call)
