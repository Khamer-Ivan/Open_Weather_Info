import timedelta
import sqlite3 as sq
from telebot import types
from telebot.types import Message
from datetime import datetime

from loader import bot

now = datetime.now()


@bot.callback_query_handler(func=lambda call: call.data.endswith('user_history'))
def weather_button(message: Message) -> None:
    start_menu = types.InlineKeyboardMarkup(row_width=1)
    for_day = types.InlineKeyboardButton(text='За день', callback_data='for_day')
    for_week = types.InlineKeyboardButton(text='За неделю', callback_data='for_week')
    for_all = types.InlineKeyboardButton(text='За всё время', callback_data='for_all')
    menu = types.InlineKeyboardButton(text='Возврат в основное меню', callback_data='menu')
    start_menu.add(for_day, for_week, for_all, menu)
    bot.send_message(
                     message.from_user.id,
                     'Пожалуйста, выберите период отображениям запросов.',
                     reply_markup=start_menu
                     )


@bot.callback_query_handler(func=lambda call: call.data.endswith('for_day'))
def history_for_day(message: Message) -> None:
    days_before = 1
    date_days_before = datetime.now() - timedelta.Timedelta(days=days_before)
    print(now.strftime("%Y-%m-%d %H:%M:%S"))
    print(date_days_before.strftime("%Y-%m-%d %H:%M:%S"))
    with sq.connect('weather.db') as con:
        cur = con.cursor()
        cur.execute(
                    f'SELECT name, request, date FROM weather '
                    f'WHERE (id = {message.from_user.id}) '
                    f'AND (date BETWEEN {date_days_before.strftime("%Y-%m-%d %H:%M:%S")} '
                    f'AND {now.strftime("%Y-%m-%d %H:%M:%S")})'
                    )
        result = cur.fetchall()
        for history in result:
            text = ''
            for emem in history:
                text += f'{emem}\n'
            bot.send_message(message.from_user.id, text)


@bot.callback_query_handler(func=lambda call: call.data.endswith('for_week'))
def history_for_week(message: Message) -> None:
    days_before = 7
    date_days_before = datetime.now() - timedelta.Timedelta(days=days_before)
    with sq.connect('weather.db') as con:
        cur = con.cursor()
        cur.execute(
                    f'SELECT name, request, date FROM weather '
                    f'WHERE id = {message.from_user.id} '
                    f'AND date BETWEEN {date_days_before.strftime("%Y-%m-%d %H:%M:%S")} '
                    f'AND {now.strftime("%Y-%m-%d %H:%M:%S")}'
                    )
        result = cur.fetchall()
        for history in result:
            text = ''
            for emem in history:
                text += f'{emem}\n'
            bot.send_message(message.from_user.id, text)


@bot.callback_query_handler(func=lambda call: call.data.endswith('for_all'))
def history_for_all(message: Message) -> None:
    with sq.connect('weather.db') as con:
        cur = con.cursor()
        cur.execute(
                    f'SELECT name, request, date FROM weather '
                    f'WHERE id = {message.from_user.id}'
                    )
        result = cur.fetchall()
        for history in result:
            text = ''
            for emem in history:
                text += f'{emem}\n'
            bot.send_message(message.from_user.id, text)
