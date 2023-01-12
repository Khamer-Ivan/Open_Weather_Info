from states.user_states import UserInfoState


def weather_image():
    if UserInfoState.language_code == 'ru':
        return {'Clear': 'Ясно ☀',
                'Clouds': 'Облачно ⛅',
                'Rain': 'Дождь 🌧',
                'Drizzle': 'Дождь 🌧',
                'Thunderstorm': 'Гроза 🌩',
                'Snow': 'Снег 🌨',
                'Mist': 'Туман 🌫'
                }
    elif UserInfoState.language_code == 'en':
        return {'Clear': 'Clear ☀',
                'Clouds': 'Clouds ⛅',
                'Rain': 'Rain 🌧',
                'Drizzle': 'Drizzle 🌧',
                'Thunderstorm': 'Thunderstorm 🌩',
                'Snow': 'Snow 🌨',
                'Mist': 'Mist 🌫'
                }
    elif UserInfoState.language_code == 'fr':
        return {'Clear': 'Clair ☀',
                'Clouds': 'Nuageux ⛅',
                'Rain': 'Pluie 🌧',
                'Drizzle': 'Pluie 🌧',
                'Thunderstorm': 'Orage 🌩',
                'Snow': 'Neige 🌨',
                'Mist': 'Brouillard 🌫'
                }
    elif UserInfoState.language_code == 'de':
        return {'Clear': 'Heiterer ☀',
                'Clouds': 'Bewölkt ⛅',
                'Rain': 'Der Regen 🌧',
                'Drizzle': 'Der Regen 🌧',
                'Thunderstorm': 'Gewitter 🌩',
                'Snow': 'Schnee 🌨',
                'Mist': 'Der Nebel 🌫'
                }
