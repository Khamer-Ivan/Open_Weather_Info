from telebot import types
from telebot.types import CallbackQuery
from loader import bot
from utils.logging_setting import logger


@bot.callback_query_handler(func=lambda call: call.data.endswith('menu'))
def main_menu(call: CallbackQuery) -> None:
    """
    Функция, предоставляющая 2 кнопки для выбора пользователем
    нужной команды: Узнать погоду и Посмотреть историю запросов.
    :param call: CallbackQuery
    :return: None
    """
    with bot.retrieve_data(call.message.chat.id) as data:
        try:
            data['user_call'] = call
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            start_menu = types.InlineKeyboardMarkup(row_width=1)
            weather_button = types.InlineKeyboardButton(
                                                        text=data['language']['weather'],
                                                        callback_data='weather_button'
                                                        )
            user_history = types.InlineKeyboardButton(
                                                        text=data['language']['history'],
                                                        callback_data='user_history'
                                                        )
            start_menu.add(weather_button, user_history)
            bot.send_message(
                            call.message.chat.id,
                            data['language']['choose_command'],
                            reply_markup=start_menu)
        except Exception as error:
            logger.error(f'User ID: {data["user_id"]} exception', exc_info=error)
            bot.send_message(data["user_id"], 'В работе бота возникла ошибка.'
                                                        '\nПопробуйте ещё раз.')