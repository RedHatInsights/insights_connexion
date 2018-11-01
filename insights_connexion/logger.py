import logging
from logging.config import dictConfig

from pythonjsonlogger import jsonlogger

from .config import config

log_config = {
    'version': 1,
    'formatters': {
        'json': {
            '()': jsonlogger.JsonFormatter,
            'fmt': '%(levelname)s %(asctime)s',
        },
    },
    'handlers': {
        'stream': {
            'level': config.log_level,
            'formatter': 'json',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'insights_connexion': {
            'handlers': ['stream'],
            'level': config.log_level,
            'propagate': True,
        }
    }
}


dictConfig(log_config)
log = logging.getLogger('insights_connexion')
