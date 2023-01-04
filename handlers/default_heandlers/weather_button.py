from telebot import types
from telebot.types import Message

from loader import bot


@bot.callback_query_handler(func=lambda call: call.data.endswith('weather_button'))
def weather_button(message: Message):
    start_menu = types.InlineKeyboardMarkup(row_width=1)
    weather_now = types.InlineKeyboardButton(text='Погода сейчас', callback_data='weather_now')
    weather_for_week = types.InlineKeyboardButton(text='Прогноз на 5 дней', callback_data='weather_for_5days')
    menu = types.InlineKeyboardButton(text='Возврат в основное меню', callback_data='menu')
    start_menu.add(weather_now, weather_for_week, menu)
    bot.send_message(message.from_user.id, 'Пожалуйста, выберите команду.', reply_markup=start_menu)
