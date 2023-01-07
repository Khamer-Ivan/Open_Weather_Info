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


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    Weather.create_table()

    start_menu = types.InlineKeyboardMarkup(row_width=2)
    english = types.InlineKeyboardButton(text='English', callback_data='en_1')
    russian = types.InlineKeyboardButton(text='Русский', callback_data='ru_1')
    francais = types.InlineKeyboardButton(text='Français', callback_data='fr_1')
    german = types.InlineKeyboardButton(text='Deutsch', callback_data='de_1')
    start_menu.add(english, russian, francais, german)
    bot.send_message(message.from_user.id,
                     f'Hello, {message.from_user.full_name},'
                     f' please select the language to work in the application.', reply_markup=start_menu)
