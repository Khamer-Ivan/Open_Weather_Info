import requests

from datetime import datetime
from telebot import types

from config_data.config import WEATHER_KEY
from loader import bot
from states.user_states import UserInfoState
from structure import weather_image


@bot.callback_query_handler(func=lambda call: call.data.endswith('now'))
def start_message(message: types.Message):
    bot.send_message(message.from_user.id,
                     f'Привет {message.from_user.first_name}'
                     f'. Напиши мне название города, и я дам тебе сводку по погоде.'
                     )

# @bot.message_handler()
def get_weather(message: types.Message):
    try:
        city_info = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={WEATHER_KEY}&units=metric'
        )
        city_data = city_info.json()

        city = city_data['name']
        cur_temp = city_data['main']['temp']
        humidity = city_data['main']['humidity']
        pressure = city_data['main']['pressure']
        wind_speed = city_data['wind']['speed']
        sunrise = datetime.fromtimestamp(city_data['sys']['sunrise'])
        sunset = datetime.fromtimestamp(city_data['sys']['sunset'])
        weather_descr = city_data['weather'][0]['main']
        day_long = sunset - sunrise

        if weather_descr in weather_image:
            description = weather_image[weather_descr]
        else:
            description = ''

        bot.send_message(message.from_user.id,
                         f'Погода в городе {city}:'
                         f'\nТемпература: {cur_temp}C° {description}'
                         f'\nВлажность: {humidity} %'
                         f'\nДавление: {pressure} мм.рт.ст.'
                         f'\nСкорость ветра: {wind_speed} м/c'
                         f'\nВосход солнца: {sunrise}'
                         f'\nЗакат: {sunset}'
                         f'\nПродолжительность светового дня: {day_long}'
                         f'\nХорошего дня! 🙂'
                         )

    except Exception:
        bot.send_message(message.from_user.id, '📝Проверьте правильность ввода города.📝')
