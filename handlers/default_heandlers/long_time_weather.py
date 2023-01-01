import requests
import math

from datetime import datetime
from telebot import types

from config_data.config import WEATHER_KEY
from loader import bot
from structure import weather_image
from states.user_states import UserInfoState
from utils.wind_description import wind_info


@bot.callback_query_handler(func=lambda call: call.data.endswith('5days'))
def start_message(message: types.Message):
    bot.send_message(message.from_user.id,
                     f'Привет {message.from_user.first_name}'
                     f'. Напиши мне название города, и я дам тебе сводку по погоде на 5 дней.'
                     )


@bot.message_handler()
def city_geolocation(message):
    city = requests.get(
                        f'http://api.openweathermap.org/geo/1.0/direct?'
                        f'q={message.text}&limit=1&appid={WEATHER_KEY}'
                        )

    city_geo = city.json()

    lat = city_geo[0]['lat']
    lon = city_geo[0]['lon']

    weather_for_week(lat, lon, message)


def weather_for_week(lat, lon, message):
    try:
        weather_list = list()
        weekly_weather = requests.get(
                                      f'http://api.openweathermap.org/data/2.5/forecast?'
                                      f'lat={lat}&lon={lon}&appid={WEATHER_KEY}&units=metric'
                                      )
        weather_data = weekly_weather.json()
        need = weather_data['list']
        for day in range(0, len(need), 8):
            date = need[day]['dt_txt']
            temp = need[day]['main']['temp']
            temp_feels_like = need[day]['main']['feels_like']
            humidity = need[day]['main']['humidity']
            pressure = need[day]['main']['pressure']
            weather_descr = need[day]['weather'][0]['main']
            wind_speed = math.ceil(need[day]['wind']['speed'])
            wind_deg = need[day]['wind']['deg']
            wind_side = wind_info(wind_deg)

            if weather_descr in weather_image:
                description = weather_image[weather_descr]
            else:
                description = ''

            weather_list.append(
                                f'Погода на {date}:'
                                f'\nТемпература: {temp}C°, ощущается как {temp_feels_like}C° {description}'
                                f'\nАтмосферное давление: {pressure} мм.рт.ст.'
                                f'\nВлажность воздуха: {humidity} %'
                                f'\nВетер {wind_side} {wind_speed} м/c'
                                )
        [bot.send_message(message.from_user.id, day_info) for day_info in weather_list]
    except Exception as error:
        bot.send_message(message.from_user.id, error)
