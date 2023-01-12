from loader import bot
from telebot.types import Message


def wind_info(message: Message, wind: int) -> str:
    """
    Функция преобразующая deg значение ветра
    в направление сторон света
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        c_1 = range(337, 380)
        c_2 = range(0, 22)
        cv = range(22, 67)
        v = range(67, 112)
        yv = range(112, 157)
        y = range(157, 202)
        yz = range(202, 247)
        z = range(247, 292)
        cz = range(292, 337)

        if wind in c_1 or wind in c_2:
            if data['language_code'] == 'ru':
                return 'Северный'
            elif data['language_code'] == 'en':
                return 'North'
            elif data['language_code'] == 'fr':
                return 'Nord'
            elif data['language_code'] == 'de':
                return 'Nordisch'
        elif wind in cv:
            if data['language_code'] == 'ru':
                return 'Северо-Восточный'
            elif data['language_code'] == 'en':
                return 'North-East'
            elif data['language_code'] == 'fr':
                return 'Nord-Est'
            elif data['language_code'] == 'de':
                return 'Nordosten'
        elif wind in v:
            if data['language_code'] == 'ru':
                return 'Восточный'
            elif data['language_code'] == 'en':
                return 'East'
            elif data['language_code'] == 'fr':
                return 'Est'
            elif data['language_code'] == 'de':
                return 'Ost'
        elif wind in yv:
            if data['language_code'] == 'ru':
                return 'Юго-Восточный'
            elif data['language_code'] == 'en':
                return 'South-East'
            elif data['language_code'] == 'fr':
                return 'Sud-Est'
            elif data['language_code'] == 'de':
                return 'Südöstlich'
        elif wind in y:
            if data['language_code'] == 'ru':
                return 'Южный'
            elif data['language_code'] == 'en':
                return 'South'
            elif data['language_code'] == 'fr':
                return 'Sud'
            elif data['language_code'] == 'de':
                return 'Südlich'
        elif wind in yz:
            if data['language_code'] == 'ru':
                return 'Юго-Западный'
            elif data['language_code'] == 'en':
                return 'South-West'
            elif data['language_code'] == 'fr':
                return 'Sud-Ouest'
            elif data['language_code'] == 'de':
                return 'Südwestlich'
        elif wind in z:
            if data['language_code'] == 'ru':
                return 'Западный'
            elif data['language_code'] == 'en':
                return 'West'
            elif data['language_code'] == 'fr':
                return 'Ouest'
            elif data['language_code'] == 'de':
                return 'Westlich'
        elif wind in cz:
            if data['language_code'] == 'ru':
                return 'Северо-Западный'
            elif data['language_code'] == 'en':
                return 'North-West'
            elif data['language_code'] == 'fr':
                return 'Nord-Ouest'
            elif data['language_code'] == 'de':
                return 'Nordwestlich'
