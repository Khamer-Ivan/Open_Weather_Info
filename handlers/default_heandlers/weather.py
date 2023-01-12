import requests
import math

from datetime import datetime
from telebot.types import CallbackQuery, Message
from googletrans import Translator

from config_data.config import WEATHER_KEY
from loader import bot
from structure import weather_image
from states.user_states import UserInfoState
from utils.wind_description import wind_info
from handlers.default_heandlers.weather_button import weather_button
from handlers.default_heandlers.start import Weather
from utils.logging_setting import exception_handler


@bot.callback_query_handler(func=lambda call: call.data.endswith('5days'))
@exception_handler
def start_message(call: CallbackQuery) -> None:
    """
    Функция, принимающая от пользователя название города, для
    предоставления информации по погоде на пять дней.
    :param call: СallbackQuery
    :return: None
    """
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    UserInfoState.flag_5_day = 1
    bot.send_message(
        call.message.chat.id, UserInfoState.language['weather_5_days'])


@bot.callback_query_handler(func=lambda call: call.data.endswith('now'))
@exception_handler
def start_message(call: CallbackQuery) -> None:
    """
    Функция, принимающая от пользователя название города для
    предоставления информации по погоде на данный момент.
    :param call: CallbackQuery
    :return: None
    """
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    UserInfoState.flag_day = 1
    bot.send_message(
        call.message.chat.id, UserInfoState.language['weather_one_day'])


@bot.message_handler()
@exception_handler
def get_weather(message: Message) -> None:
    """
    Функция, принимающая название города, и предоставляющая
    информацию по погоде, на период, выбранный пользователем.
    :param message:
    :return: None
    """
    if UserInfoState.flag_day == 1:
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
        translation = Translator()
        city = translation.translate(text=city, src='en', dest=UserInfoState.language_code).text
        weather_img = weather_image()
        if weather_descr in weather_img:
            description = weather_img[weather_descr]
        else:
            description = ''

        result = (f'{UserInfoState.language["res_0"]} {city}:'
                  f'\n'
                  f'\n🔹 {UserInfoState.language["res_1"]} {math.ceil(cur_temp)}C° {description}'
                  f'\n🔹 {UserInfoState.language["res_2"]} {humidity} %'
                  f'\n🔹 {UserInfoState.language["res_3"]} {pressure} {UserInfoState.language["res_4"]}'
                  f'\n🔹 {UserInfoState.language["res_5"]} {wind_side},'
                  f' {wind_speed} {UserInfoState.language["res_6"]}'
                  f'\n🔹 {UserInfoState.language["res_7"]} {sunrise}'
                  f'\n🔹 {UserInfoState.language["res_8"]} {sunset}'
                  f'\n🔹 {UserInfoState.language["res_9"]} {day_long}'
                  f'\n'
                  f'\n{UserInfoState.language["res_10"]}'
                  ),
        bot.send_message(
            message.from_user.id, result)
        UserInfoState.flag_day = 0
        text = f'{UserInfoState.language["log_day"]} {city}'
        Weather.create(
            user_id=message.from_user.id, name=message.from_user.full_name,
            request=text, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        weather_button(UserInfoState.user_call)

    elif UserInfoState.flag_5_day == 1:
        city = requests.get(
            f'http://api.openweathermap.org/geo/1.0/direct?'
            f'q={message.text}&limit=1&appid={WEATHER_KEY}'
        )

        city_geo = city.json()

        city_name = city_geo[0]['local_names']['ru']
        lat = city_geo[0]['lat']
        lon = city_geo[0]['lon']

        weather_for_week(city_name, lat, lon, message)


@exception_handler
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
    weather_list = list()
    weekly_weather = requests.get(
        f'http://api.openweathermap.org/data/2.5/forecast?'
        f'lat={lat}&lon={lon}&appid={WEATHER_KEY}&units=metric'
    )
    translation = Translator()
    city = translation.translate(text=city, src='en', dest=UserInfoState.language_code).text
    weather_data = weekly_weather.json()
    weather_list.append(f'{UserInfoState.language["log_five"]} {city}')
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
        weather_img = weather_image()
        if weather_descr in weather_img:
            description = weather_img[weather_descr]
        else:
            description = ''
        result = (f'{UserInfoState.language["res_five_day_0"]} {date}:'
                  f'\n🔹{UserInfoState.language["res_1"]} {math.ceil(temp)}C°, '
                  f'{UserInfoState.language["res_five_day_1"]} {math.ceil(temp_feels_like)}C° {description}'
                  f'\n🔹{UserInfoState.language["res_3"]} {pressure} {UserInfoState.language["res_4"]}'
                  f'\n🔹{UserInfoState.language["res_2"]} {humidity} %'
                  f'\n🔹{UserInfoState.language["res_5"]} {wind_side} '
                  f'{wind_speed} {UserInfoState.language["res_6"]}'
                  )
        weather_list.append(result)
    UserInfoState.flag_5_day = 0
    text = ''
    for day_info in weather_list:
        text += f'\n{day_info}\n'
    bot.send_message(message.from_user.id, text)
    text = f'{UserInfoState.language["log_five"]}{city}'
    Weather.create(
        user_id=message.from_user.id, name=message.from_user.full_name,
        request=text, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    weather_button(UserInfoState.user_call)
