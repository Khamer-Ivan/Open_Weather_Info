from telebot import types
from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    """
    Функция инициализации Inline кнопок, передающая ответ в weather или long_time_weather
    :param message:
    :return:
    """
    start_menu = types.InlineKeyboardMarkup()
    weather_now = types.InlineKeyboardButton(text='Погода сейчас', callback_data='weather_now')
    weather_for_week = types.InlineKeyboardButton(text='Прогноз на 5 дней', callback_data='weather_for_5days')
    start_menu.add(weather_now, weather_for_week)
    bot.send_message(message.from_user.id, 'Пожалуйста, выберите команду.', reply_markup=start_menu)
