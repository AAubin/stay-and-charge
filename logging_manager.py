import logging.config
import logging

def setup_logging():
    config_dict = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'level': logging.DEBUG,
            },
            'file': {
                'class': 'logging.FileHandler',
                'formatter': 'standard',
                'filename': 'app.log',
                'level': logging.INFO,
            }
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['console'],
                'level': logging.WARNING,
                'propagate': False
            },
            'data': {
                    'handlers': ['console'],
                    'level': logging.DEBUG,
                    'propagate': False
            },
            'services': {
                    'handlers': ['console'],
                    'level': logging.DEBUG,
                    'propagate': False
            },
            'components': {
                    'handlers': ['console'],
                    'level': logging.DEBUG,
                    'propagate': False
            },
            'models': {
                    'handlers': ['console'],
                    'level': logging.DEBUG,
                    'propagate': False
            }
        }
    }

    logging.config.dictConfig(config_dict)

def debugging(func):
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        logger.debug(f"Entering: {func.__name__} with args: {args} kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logger.debug(f"Exiting: {func.__name__} with result: {result}")
        return result
    return wrapper
