from datetime import datetime
from timedelta import Timedelta
from telebot.types import Message

from loader import bot
from handlers.default_heandlers.start import Weather
from handlers.default_heandlers.start import bot_start
from states.user_states import UserInfoState
from translation import translator as tr


@bot.callback_query_handler(func=lambda call: call.data.endswith('delete_day'))
def delete_day(message: Message) -> None:
    message_counter = 0
    for history in Weather.select().where(
            (Weather.user_id == message.from_user.id)
            & (Weather.date.startswith(datetime.now().strftime("%Y-%m-%d")))):
        history.delete_instance()
        message_counter += 1
    bot.send_message(message.from_user.id, tr(f'История запросов за выбранный период очищена.'
                                              f'Удалено запросов: {message_counter}', 'ru', UserInfoState.language)
                     )
    bot_start(message)


@bot.callback_query_handler(func=lambda call: call.data.endswith('delete_week'))
def delete_week(message: Message) -> None:
    message_counter = 0
    date_days_before = datetime.now() - Timedelta(days=7)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    week_ago = date_days_before.strftime("%Y-%m-%d %H:%M:%S")
    for history in Weather.select().where(
            (Weather.user_id == message.from_user.id)
            & (Weather.date.between(week_ago, now))):
        history.delete_instance()
        message_counter += 1
    bot.send_message(message.from_user.id, tr(f'История запросов за выбранный период очищена.'
                                              f'Удалено запросов: {message_counter}', 'ru', UserInfoState.language)
                     )
    bot_start(message)


@bot.callback_query_handler(func=lambda call: call.data.endswith('delete_all'))
def delete_all(message: Message) -> None:
    message_counter = 0
    for history in Weather.select().where(Weather.user_id == message.from_user.id):
        history.delete_instance()
        message_counter += 1
    bot.send_message(message.from_user.id, tr(f'История запросов за выбранный период очищена.'
                                              f'Удалено запросов: {message_counter}', 'ru', UserInfoState.language)
                     )
    bot_start(message)
