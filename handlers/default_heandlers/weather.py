import requests
import math
import sqlite3 as sq

from datetime import datetime
from telebot import types

from config_data.config import WEATHER_KEY
from loader import bot
from structure import weather_image
from states.user_states import UserInfoState
from utils.wind_description import wind_info
from handlers.default_heandlers.weather_button import weather_button

now = datetime.now()


@bot.callback_query_handler(func=lambda call: call.data.endswith('5days'))
def start_message(message: types.Message):
    """
    Функция, принимающая от пользователя название города
    :param message:
    :return:
    """
    UserInfoState.five_days = 1
    bot.send_message(message.from_user.id,
                     'Напиши мне название города, и я дам тебе сводку по погоде на 5 дней.'
                     )


@bot.callback_query_handler(func=lambda call: call.data.endswith('now'))
def start_message(message: types.Message) -> None:
    """
    Функция, принимающая от пользователя название города
    :param message:
    :return: None
    """
    UserInfoState.day = 1
    bot.send_message(message.from_user.id,
                     'Напиши мне название города, и я дам тебе сводку по погоде.'
                     )


@bot.message_handler()
def get_weather(message: types.Message) -> None:
    """
    Функция, принимающая название города,
    и выдающая сводку по погоде в данный момент.
    :param message:
    :return: None
    """
    if UserInfoState.day == 1:
        try:
            city_info = requests.get(
                                     f'https://api.openweathermap.org/data/2.5/weather?'
                                     f'q={message.text}&appid={WEATHER_KEY}&units=metric'
                                     )
            city_data = city_info.json()

            city = city_data['name']
            cur_temp = city_data['main']['temp']
            humidity = city_data['main']['humidity']
            pressure = city_data['main']['pressure']
            wind_speed = city_data['wind']['speed']
            wind_deg = city_data['wind']['deg']
            sunrise = datetime.fromtimestamp(city_data['sys']['sunrise'])
            sunset = datetime.fromtimestamp(city_data['sys']['sunset'])
            weather_descr = city_data['weather'][0]['main']
            day_long = sunset - sunrise
            wind_side = wind_info(wind_deg)

            if weather_descr in weather_image:
                description = weather_image[weather_descr]
            else:
                description = ''

            bot.send_message(message.from_user.id,
                             f'Погода в городе {city}:'
                             f'\n'
                             f'\n🔹 Температура: {int(cur_temp)}C° {description}'
                             f'\n🔹 Влажность: {humidity} %'
                             f'\n🔹 Давление: {pressure} мм.рт.ст.'
                             f'\n🔹 Ветер {wind_side}, {wind_speed} м/c'
                             f'\n🔹 Восход солнца: {sunrise}'
                             f'\n🔹 Закат: {sunset}'
                             f'\n🔹 Продолжительность светового дня: {day_long}'
                             f'\n'
                             f'\n😊 ХОРОШЕГО ДНЯ'
                             )
            UserInfoState.day = 0
            with sq.connect('weather.db') as con:
                cur = con.cursor()
                text = f'Запрос текущей погоды в городе {city}'
                cur.execute('INSERT INTO weather VALUES(?,?,?,?);',
                            (
                             message.from_user.id,
                             message.from_user.full_name,
                             text,
                             now.strftime("%Y-%m-%d %H:%M:%S")
                            )
                            )
            weather_button(message)

        except Exception:
            bot.send_message(message.from_user.id, '📝Проверьте правильность ввода города.📝')
    elif UserInfoState.five_days == 1:
        try:
            city = requests.get(
                                f'http://api.openweathermap.org/geo/1.0/direct?'
                                f'q={message.text}&limit=1&appid={WEATHER_KEY}'
                                )

            city_geo = city.json()

            city_name = city_geo[0]['local_names']['ru']
            lat = city_geo[0]['lat']
            lon = city_geo[0]['lon']

            weather_for_week(city_name, lat, lon, message)
        except Exception:
            bot.send_message(message.from_user.id, '📝Проверьте правильность ввода города.📝')


def weather_for_week(city, lat, lon, message: types.Message) -> None:
    """
        Функция, принимающая значения широты и долготы, и передающая их
        для получения длительного прогноза погоды
        :param city: Город
        :param lat: Широта
        :param lon: Долгота
        :param message:
        :return: None
        """
    try:
        weather_list = list()
        weekly_weather = requests.get(
            f'http://api.openweathermap.org/data/2.5/forecast?'
            f'lat={lat}&lon={lon}&appid={WEATHER_KEY}&units=metric'
        )
        weather_data = weekly_weather.json()
        weather_list.append('Погода в городе {} на 5 дней'.format(city))
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
                                f'\n🔹Температура: {int(temp)}C°, ощущается как {int(temp_feels_like)}C° {description}'
                                f'\n🔹Атмосферное давление: {pressure} мм.рт.ст.'
                                f'\n🔹Влажность воздуха: {humidity} %'
                                f'\n🔹Ветер {wind_side} {wind_speed} м/c'
                                )
        UserInfoState.five_days = 0
        [bot.send_message(message.from_user.id, day_info) for day_info in weather_list]
        with sq.connect('weather.db') as con:
            cur = con.cursor()
            text = f'Запрос погоды на 5 дней в городе {city}'
            cur.execute('INSERT INTO weather VALUES(?,?,?,?);',
                        (
                            message.from_user.id,
                            message.from_user.full_name,
                            text,
                            now.strftime("%Y-%m-%d %H:%M:%S")
                        )
                        )
        weather_button(message)

    except Exception:
        bot.send_message(message.from_user.id, '📝Проверьте правильность ввода города.📝')
