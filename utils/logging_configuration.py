"""
Файл с настройкой конфигурации логгера.
"""

import logging
import logging.config


class FilterError(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.ERROR


dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(filename)s | %(funcName)s | %(lineno)s | %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "base",
        },
        "info": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "when": "H",
            "interval": 24,
            "formatter": "base",
            "filename": "debug.log",
        },
    },
    "loggers": {
        "bot_logger": {
            "level": "INFO",
            "handlers": ["console", "info"]
        },
    },
    "filters": {
        "error": {
            "()": FilterError
        }
    }
}


def custom_logger(logger_name: str) -> logging.Logger:
    """
    Функция - для применения конфигураций Логгера по настройкам
    :param logger_name: str
    :return: Logger
    """
    logging.config.dictConfig(dict_config)
    logger = logging.getLogger(logger_name)
    return logger
