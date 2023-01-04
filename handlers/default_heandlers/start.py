import sqlite3 as sq

from telebot import types
from telebot.types import Message

from loader import bot


@bot.callback_query_handler(func=lambda call: call.data.endswith('menu'))
@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    """
    Функция инициализации Inline кнопок, передающая ответ в weather или long_time_weather
    :param message:
    :return:
    """
    with sq.connect('weather.db') as con:
        cur = con.cursor()

        # cur.execute('DROP TABLE IF EXISTS weather')
        cur.execute(
            """
                    CREATE TABLE IF NOT EXISTS weather
                    (
                    id INTEGER,
                    name TEXT,
                    request TEXT,
                    date DATETIME
                    )
                    """
        )

    start_menu = types.InlineKeyboardMarkup(row_width=1)
    weather_button = types.InlineKeyboardButton(text='Узнать погоду', callback_data='weather_button')
    user_history = types.InlineKeyboardButton(text='История запросов', callback_data='user_history')
    start_menu.add(weather_button, user_history)
    bot.send_message(message.from_user.id,
                     f'Привет {message.from_user.first_name}. Пожалуйста, выберите команду.', reply_markup=start_menu)
