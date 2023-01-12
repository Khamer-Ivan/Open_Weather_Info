from states.user_states import UserInfoState
from loader import bot
from telebot.types import Message


def weather_image(message: Message) -> dict:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if data['language_code'] == 'ru':
            return {'Clear': 'Ясно ☀',
                    'Clouds': 'Облачно ⛅',
                    'Rain': 'Дождь 🌧',
                    'Drizzle': 'Дождь 🌧',
                    'Thunderstorm': 'Гроза 🌩',
                    'Snow': 'Снег 🌨',
                    'Mist': 'Туман 🌫'
                    }
        elif data['language_code'] == 'en':
            return {'Clear': 'Clear ☀',
                    'Clouds': 'Clouds ⛅',
                    'Rain': 'Rain 🌧',
                    'Drizzle': 'Drizzle 🌧',
                    'Thunderstorm': 'Thunderstorm 🌩',
                    'Snow': 'Snow 🌨',
                    'Mist': 'Mist 🌫'
                    }
        elif data['language_code'] == 'fr':
            return {'Clear': 'Clair ☀',
                    'Clouds': 'Nuageux ⛅',
                    'Rain': 'Pluie 🌧',
                    'Drizzle': 'Pluie 🌧',
                    'Thunderstorm': 'Orage 🌩',
                    'Snow': 'Neige 🌨',
                    'Mist': 'Brouillard 🌫'
                    }
        elif data['language_code'] == 'de':
            return {'Clear': 'Heiterer ☀',
                    'Clouds': 'Bewölkt ⛅',
                    'Rain': 'Der Regen 🌧',
                    'Drizzle': 'Der Regen 🌧',
                    'Thunderstorm': 'Gewitter 🌩',
                    'Snow': 'Schnee 🌨',
                    'Mist': 'Der Nebel 🌫'
                    }
