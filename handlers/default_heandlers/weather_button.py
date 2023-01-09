from telebot import types
from telebot.types import Message, CallbackQuery

from loader import bot
from states.user_states import UserInfoState


@bot.callback_query_handler(func=lambda call: call.data.endswith('weather_button'))
def weather_button(message: Message):
    # bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

    start_menu = types.InlineKeyboardMarkup(row_width=1)
    weather_now = types.InlineKeyboardButton(
                                                text=UserInfoState.language['weather_now'],
                                                callback_data='weather_now'
                                             )
    weather_for_week = types.InlineKeyboardButton(
                                                    text=UserInfoState.language['weather_for_five'],
                                                    callback_data='weather_for_5days'
                                                  )
    menu = types.InlineKeyboardButton(
                                        text=UserInfoState.language['back_menu'],
                                        callback_data='menu'
                                      )
    start_menu.add(weather_now, weather_for_week, menu)
    bot.send_message(
                        message.from_user.id, UserInfoState.language['choose_command'],
                        reply_markup=start_menu,
                    )
