import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEATHER_KEY = os.getenv('WEATHER_KEY')
DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('history', "Вывести историю")
)
