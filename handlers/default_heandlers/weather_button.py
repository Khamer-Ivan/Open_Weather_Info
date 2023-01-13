from telebot import types
from telebot.types import CallbackQuery

from loader import bot


@bot.callback_query_handler(func=lambda call: call.data.endswith('weather_button'))
def weather_button(call: CallbackQuery) -> None:
    """
    Функция, предоставляющая в виде inline кнопок выбор
    периода информирования по погоде.
    :param call: CallbackQuery
    :return: None
    """

    with bot.retrieve_data(call.message.chat.id) as data:
        start_menu = types.InlineKeyboardMarkup(row_width=1)
        weather_now = types.InlineKeyboardButton(
                                                    text=data['language']['weather_now'],
                                                    callback_data='weather_now'
                                                 )
        weather_for_week = types.InlineKeyboardButton(
                                                        text=data['language']['weather_for_five'],
                                                        callback_data='weather_for_5days'
                                                      )
        menu = types.InlineKeyboardButton(
                                            text=data['language']['back_menu'],
                                            callback_data='menu'
                                          )
        start_menu.add(weather_now, weather_for_week, menu)
        bot.send_message(
                            call.message.chat.id, data['language']['choose_command'],
                            reply_markup=start_menu,
                        )
