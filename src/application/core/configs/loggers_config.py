import os
from logging import DEBUG, ERROR


def get_logging(logs_dir: str) -> dict:
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '%(message)s',
            },
            'verbose': {
                'format': (
                    '%(levelname)s %(asctime)s.%(msecs)03d %(pathname)s '
                    '%(funcName)s %(lineno)d %(process)d %(thread)d %(message)s'
                ),
                'datefmt': '%d/%m/%Y %H:%M:%S',
            },
            'json': {
                '()': 'json_log_formatter.JSONFormatter',
            },
        },
        'handlers': {
            'request.5XX': {
                'level': DEBUG,
                'class': 'logging.FileHandler',
                'filename': os.path.join(logs_dir, '5XX.json'),
                'formatter': 'json',
            },
            'request.4XX': {
                'level': DEBUG,
                'class': 'logging.FileHandler',
                'filename': os.path.join(logs_dir, '4XX.json'),
                'formatter': 'json',
            },
            'console': {
                'level': DEBUG,
                'class': 'logging.StreamHandler',
                'formatter': 'json',
            }
        },
        'loggers': {
            'request.5XX': {
                'handlers': ['request.5XX', 'console'],
                'level': ERROR,
            },
            'request.4XX': {
                'handlers': ['request.4XX', 'console'],
                'level': ERROR,
            }
        }
    }
