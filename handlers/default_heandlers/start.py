from telebot import types
from telebot.types import Message, CallbackQuery

from loader import bot
from database.database import Weather
from states.user_states import UserInfoState
from languages import russian, english, german, french
from handlers.default_heandlers.menu import main_menu


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    Weather.create_table()

    UserInfoState.user_id = message.from_user.id
    UserInfoState.user_full_name = message.from_user.full_name
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
    if call.data.startswith('ru'):
        UserInfoState.language = russian.translation
        UserInfoState.language_code = 'ru'
    elif call.data.startswith('en'):
        UserInfoState.language = english.translation
        UserInfoState.language_code = 'en'
    elif call.data.startswith('fr'):
        UserInfoState.language = french.translation
        UserInfoState.language_code = 'fr'
    elif call.data.startswith('de'):
        UserInfoState.language = german.translation
        UserInfoState.language_code = 'de'
    main_menu(call)

