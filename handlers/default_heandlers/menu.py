from telebot import types
from telebot.types import Message, CallbackQuery
from states.user_states import UserInfoState
from translation import translator

from loader import bot


@bot.callback_query_handler(func=lambda call: call.data.endswith('menu'))
@bot.callback_query_handler(func=lambda call: call.data.endswith('_1'))
def main_menu(call: CallbackQuery):
    if not call.data.startswith('menu'):
        UserInfoState.language = call.data[:2]
    start_menu = types.InlineKeyboardMarkup(row_width=1)
    weather_button = types.InlineKeyboardButton(
                                                text=translator('Узнать погоду', 'ru', UserInfoState.language),
                                                callback_data='weather_button'
                                                )
    user_history = types.InlineKeyboardButton(
                                                text=translator('История запросов', 'ru', UserInfoState.language),
                                                callback_data='user_history'
                                                )
    start_menu.add(weather_button, user_history)
    bot.send_message(
                    call.message.chat.id,
                    translator('Пожалуйста, выберите команду.', 'ru', UserInfoState.language),
                    reply_markup=start_menu)
