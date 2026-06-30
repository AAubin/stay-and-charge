import logging.config
import logging

def setup_logging():
    """Configure le logging global — à appeler en premier dans app.py avant tout autre import."""
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
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['console'],
                'level': logging.INFO,
                'propagate': False
            },
            'data': {
                'handlers': ['console'],
                'level': logging.INFO,
                'propagate': False
            },
            'services': {
                'handlers': ['console'],
                'level': logging.INFO,
                'propagate': False
            },
            'components': {
                'handlers': ['console'],
                'level': logging.INFO,
                'propagate': False
            },
            'models': {
                'handlers': ['console'],
                'level': logging.INFO,
                'propagate': False
            },
            'streamlit': {
                'handlers': ['console'],
                'level': logging.ERROR,
                'propagate': False
            }
        }
    }

    logging.config.dictConfig(config_dict)

def debugging(func):
    """Décorateur qui loggue l'entrée et la sortie d'une fonction en mode DEBUG.

    Args:
        func: fonction à décorer.
    Returns:
        fonction wrappée avec logs DEBUG sur les args et le résultat.
    """
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        logger.debug(f"Entering: {func.__name__} with args: {args} kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logger.debug(f"Exiting: {func.__name__} with result: {result}")
        return result
    return wrapper
