from peewee import *
from telebot import types
from telebot.types import Message

from loader import bot

db = SqliteDatabase('weather.db')


class Weather(Model):
    user_id = IntegerField()
    name = CharField()
    request = CharField()
    date = CharField()

    class Meta:
        database = db


@bot.callback_query_handler(func=lambda call: call.data.endswith('menu'))
@bot.message_handler(commands=['start'])
def bot_start(message: Message):

    Weather.create_table()

    start_menu = types.InlineKeyboardMarkup(row_width=1)
    weather_button = types.InlineKeyboardButton(text='Узнать погоду', callback_data='weather_button')
    user_history = types.InlineKeyboardButton(text='История запросов', callback_data='user_history')
    start_menu.add(weather_button, user_history)
    bot.send_message(message.from_user.id,
                     f'Привет {message.from_user.first_name}. Пожалуйста, выберите команду.', reply_markup=start_menu)
