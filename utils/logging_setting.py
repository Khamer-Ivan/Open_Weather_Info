from loguru import logger
from typing import Callable
from loader import bot
from states.user_states import UserInfoState


logger.add('debug.log', format='{time} {level} {message}',
           level='DEBUG', rotation='100 KB', compression='zip')


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
            logger.error(f'В работе бота возникло исключение {error}')
            bot.send_message(UserInfoState.user_id, 'В работе программы что-то пошло не так.'
                                                    'Давайте попробуем ещё раз.')

    return wrapped_func
