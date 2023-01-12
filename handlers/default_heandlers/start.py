from telebot import types
from telebot.types import Message, CallbackQuery

from loader import bot
from database.database import Weather
from states.user_states import UserInfoState
from languages import russian, english, german, french
from handlers.default_heandlers.menu import main_menu


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    """
    Функция, предоставляющая в виде inline кнопок выбор
    одного из четырёх языков для работы.
    :param message: Message
    :return: None
    """
    Weather.create_table()

    bot.set_state(message.from_user.id, UserInfoState.language, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['user_id'] = message.from_user.id
        data['user_full_name'] = message.from_user.full_name
    start_menu = types.InlineKeyboardMarkup(row_width=2)
    eng = types.InlineKeyboardButton(text='English', callback_data='en_1')
    rus = types.InlineKeyboardButton(text='Русский', callback_data='ru_1')
    fran = types.InlineKeyboardButton(text='Français', callback_data='fr_1')
    ger = types.InlineKeyboardButton(text='Deutsch', callback_data='de_1')
    start_menu.add(eng, rus, fran, ger)
    bot.send_message(message.from_user.id,
                     f'Hello, {message.from_user.full_name},'
                     f' please select the language to work in the application.', reply_markup=start_menu)


@bot.callback_query_handler(func=lambda call: call.data.endswith('_1'))
def choose_lang(call: CallbackQuery) -> None:
    """
    Функция, принимающая ответ пользователя для
    обработки языка дальнейшей работы бота.
    :param call: CallbackQuery
    :return: None
    """
    with bot.retrieve_data(call.message.chat.id) as data:
        if call.data.startswith('ru'):
            data['language'] = russian.translation
            data['language_code'] = 'ru'
        elif call.data.startswith('en'):
            data['language'] = english.translation
            data['language_code'] = 'en'
        elif call.data.startswith('fr'):
            data['language'] = french.translation
            data['language_code'] = 'fr'
        elif call.data.startswith('de'):
            data['language'] = german.translation
            data['language_code'] = 'de'

    main_menu(call)

