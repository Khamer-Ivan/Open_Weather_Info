from telebot import types
from telebot.types import Message

from loader import bot
from handlers.default_heandlers.start import Weather


def delete_day(message: Message):
    delete_day_menu = types.InlineKeyboardMarkup(row_width=1)
    delete_button = types.InlineKeyboardButton(text='Удалить историю за день', callback_data='delete_day')
    user_history = types.InlineKeyboardButton(text='Возврат в основное меню', callback_data='menu')
    delete_day_menu.add(delete_button, user_history)
    bot.send_message(message.from_user.id, 'Пожалуйста, выберите команду.', reply_markup=delete_day_menu)


def delete_week(message: Message):
    delete_week_menu = types.InlineKeyboardMarkup(row_width=1)
    delete_button = types.InlineKeyboardButton(text='Удалить историю за неделю', callback_data='delete_week')
    user_history = types.InlineKeyboardButton(text='Возврат в основное меню', callback_data='menu')
    delete_week_menu.add(delete_button, user_history)
    bot.send_message(message.from_user.id, 'Пожалуйста, выберите команду.', reply_markup=delete_week_menu)


def delete_all(message: Message):
    delete_all_menu = types.InlineKeyboardMarkup(row_width=1)
    delete_button = types.InlineKeyboardButton(text='Удалить историю запросов', callback_data='delete_all')
    user_history = types.InlineKeyboardButton(text='Возврат в основное меню', callback_data='menu')
    delete_all_menu.add(delete_button, user_history)
    bot.send_message(message.from_user.id, 'Пожалуйста, выберите команду.', reply_markup=delete_all_menu)
