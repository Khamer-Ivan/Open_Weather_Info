from telebot import types
from telebot.types import CallbackQuery
from states.user_states import UserInfoState
from loader import bot
from utils.logging_setting import exception_handler


@bot.callback_query_handler(func=lambda call: call.data.endswith('menu'))
@exception_handler
def main_menu(call: CallbackQuery) -> None:
    """
    Функция, предоставляющая 2 кнопки для выбора пользователем
    нужной команды: Узнать погоду и Посмотреть историю запросов.
    :param call: CallbackQuery
    :return: None
    """
    UserInfoState.user_call = call
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    start_menu = types.InlineKeyboardMarkup(row_width=1)
    weather_button = types.InlineKeyboardButton(
                                                text=UserInfoState.language['weather'],
                                                callback_data='weather_button'
                                                )
    user_history = types.InlineKeyboardButton(
                                                text=UserInfoState.language['history'],
                                                callback_data='user_history'
                                                )
    start_menu.add(weather_button, user_history)
    bot.send_message(
                    call.message.chat.id,
                    UserInfoState.language['choose_command'],
                    reply_markup=start_menu)
