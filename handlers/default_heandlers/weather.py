import requests
import math

from datetime import datetime
from telebot.types import CallbackQuery, Message
from googletrans import Translator

from config_data.config import WEATHER_KEY
from loader import bot
from structure import weather_image
from utils.wind_description import wind_info
from handlers.default_heandlers.weather_button import weather_button
from handlers.default_heandlers.start import Weather
from utils.logging_setting import logger


@bot.callback_query_handler(func=lambda call: call.data.endswith('5days'))
def start_message(call: CallbackQuery) -> None:
    """
    Функция, принимающая от пользователя название города, для
    предоставления информации по погоде на пять дней.
    :param call: СallbackQuery
    :return: None
    """
    with bot.retrieve_data(call.message.chat.id) as data:
        try:
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            data['flag_5_day'] = 1
            bot.send_message(
                call.message.chat.id, data['language']['weather_5_days'])
        except Exception as error:
            logger.error(f'User ID: {data["user_id"]} exception', exc_info=error)
            bot.send_message(data["user_id"], 'В работе бота возникла ошибка.'
                                              '\nПопробуйте ещё раз.')


@bot.callback_query_handler(func=lambda call: call.data.endswith('now'))
def start_message(call: CallbackQuery) -> None:
    """
    Функция, принимающая от пользователя название города для
    предоставления информации по погоде на данный момент.
    :param call: CallbackQuery
    :return: None
    """
    with bot.retrieve_data(call.message.chat.id) as data:
        try:
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            data['flag_day'] = 1
            bot.send_message(
                call.message.chat.id, data['language']['weather_one_day'])
        except Exception as error:
            logger.error(f'User ID: {data["user_id"]} exception', exc_info=error)
            bot.send_message(data["user_id"], 'В работе бота возникла ошибка.'
                                              '\nПопробуйте ещё раз.')


@bot.message_handler()
def get_weather(message: Message) -> None:
    """
    Функция, принимающая название города, и предоставляющая
    информацию по погоде, на период, выбранный пользователем.
    :param message:
    :return: None
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        try:
            if data['flag_day'] == 1:
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
                wind_side = wind_info(message, wind_deg)
                translation = Translator()
                city = translation.translate(text=city, src='en', dest=data['language_code']).text
                weather_img = weather_image(message)
                if weather_descr in weather_img:
                    description = weather_img[weather_descr]
                else:
                    description = ''

                result = (f'{data["language"]["res_0"]} {city}:'
                          f'\n'
                          f'\n🔹 {data["language"]["res_1"]} {math.ceil(cur_temp)}C° {description}'
                          f'\n🔹 {data["language"]["res_2"]} {humidity} %'
                          f'\n🔹 {data["language"]["res_3"]} {pressure} {data["language"]["res_4"]}'
                          f'\n🔹 {data["language"]["res_5"]} {wind_side},'
                          f' {wind_speed} {data["language"]["res_6"]}'
                          f'\n🔹 {data["language"]["res_7"]} {sunrise}'
                          f'\n🔹 {data["language"]["res_8"]} {sunset}'
                          f'\n🔹 {data["language"]["res_9"]} {day_long}'
                          f'\n'
                          f'\n{data["language"]["res_10"]}'
                          ),
                bot.send_message(
                    message.from_user.id, result)
                data['flag_day'] = 0
                text = f'{data["language"]["log_day"]} {city}'
                Weather.create(
                    user_id=message.from_user.id, name=message.from_user.full_name,
                    request=text, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                weather_button(data['user_call'])

            elif data['flag_5_day'] == 1:
                city = requests.get(
                    f'http://api.openweathermap.org/geo/1.0/direct?'
                    f'q={message.text}&limit=1&appid={WEATHER_KEY}'
                )

                city_geo = city.json()

                city_name = city_geo[0]['local_names']['ru']
                lat = city_geo[0]['lat']
                lon = city_geo[0]['lon']

                weather_for_week(city_name, lat, lon, message)
        except Exception as error:
            logger.error(f'User ID: {data["user_id"]} exception', exc_info=error)
            bot.send_message(data["user_id"], 'В работе бота возникла ошибка.'
                                              '\nПопробуйте ещё раз.')


def weather_for_week(city, lat, lon, message: Message) -> None:
    """
        Функция, принимающая значения широты и долготы, и передающая их
        для получения длительного прогноза погоды
        :param city: Город
        :param lat: Широта
        :param lon: Долгота
        :param message:
        :return: None
        """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        try:
            weather_list = list()
            weekly_weather = requests.get(
                f'http://api.openweathermap.org/data/2.5/forecast?'
                f'lat={lat}&lon={lon}&appid={WEATHER_KEY}&units=metric'
            )
            translation = Translator()
            city = translation.translate(text=city, src='en', dest=data['language_code']).text
            weather_data = weekly_weather.json()
            weather_list.append(f'{data["language"]["log_five"]} {city}')
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
                wind_side = wind_info(message, wind_deg)
                weather_img = weather_image(message)
                if weather_descr in weather_img:
                    description = weather_img[weather_descr]
                else:
                    description = ''
                result = (f'{data["language"]["res_five_day_0"]} {date}:'
                          f'\n🔹{data["language"]["res_1"]} {math.ceil(temp)}C°, '
                          f'{data["language"]["res_five_day_1"]} {math.ceil(temp_feels_like)}C° {description}'
                          f'\n🔹{data["language"]["res_3"]} {pressure} {data["language"]["res_4"]}'
                          f'\n🔹{data["language"]["res_2"]} {humidity} %'
                          f'\n🔹{data["language"]["res_5"]} {wind_side} '
                          f'{wind_speed} {data["language"]["res_6"]}'
                          )
                weather_list.append(result)
            data['flag_5_day'] = 0
            text = ''
            for day_info in weather_list:
                text += f'\n{day_info}\n'
            bot.send_message(message.from_user.id, text)
            text = f'{data["language"]["log_five"]}{city}'
            Weather.create(
                user_id=message.from_user.id, name=message.from_user.full_name,
                request=text, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            weather_button(data['user_call'])
        except Exception as error:
            logger.error(f'User ID: {data["user_id"]} exception', exc_info=error)
            bot.send_message(data["user_id"], 'В работе бота возникла ошибка.'
                                              '\nПопробуйте ещё раз.')
