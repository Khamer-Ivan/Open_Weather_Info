"""
Файл для создания экземпляров: бота и логгера.
Так же содержит декоратор для отлова исключений и логгирования ошибок
"""

from utils.logging_configuration import custom_logger

logger = custom_logger('bot_logger')

