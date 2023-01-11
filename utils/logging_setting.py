"""
Файл для создания экземпляров: бота и логгера.
Так же содержит декоратор для отлова исключений и логгирования ошибок
"""
from typing import Callable

from requests import ReadTimeout
from states.user_states import UserInfoState
from utils.logging_configuration import custom_logger
from loader import bot

logger = custom_logger('bot_logger')


def exception_handler(func: Callable) -> Callable:
    """
    Декоратор - оборачивающий функцию в try-except блок.
    :param func: Callable
    :return: Callable
    """
    def wrapped_func(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as error:
            logger.error(f'User ID: {UserInfoState.user_id} exception', exc_info=error)
            bot.send_message(UserInfoState.user_id, 'В работе бота возникла ошибка.'
                                                    '\nПопробуйте ещё раз.')
    return wrapped_func


def exception_request_handler(func: Callable) -> Callable:
    """
    Декоратор - оборачивающий функцию request в try-except блок.
    :param func: Callable
    :return: Callable
    """
    def wrapped_func(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except (ConnectionError, TimeoutError, ReadTimeout) as error:
            logger.error(f'User ID: {UserInfoState.user_id} exception', exc_info=error)
            bot.send_message(UserInfoState.user_id, 'В работе бота возникла ошибка.'
                                                    '\nПопробуйте ещё раз.')
    return wrapped_func
