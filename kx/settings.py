#_*_coding:utf-8_*_

import os

# RUN_ENV = dev or test or deploy
RUN_ENV = os.getenv("RUN_ENV",default='dev')

ROOT_DIR = os.path.dirname(__file__)

EMAIL = 'mrmuxl@sina.com'
ADMINS = (
    ('admin', EMAIL),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = ['simplenect.cn','www.simplenect.cn','www.qianmo.cc','qianmo.cc','localhost']

THEME = '/default/'

DOMAIN = 'http://www.simplenect.cn'

LOGIN_URL = '/User/login/'
LOGOUT_URL='/User/logout/'
LOGIN_REDIRECT_URL = LOGIN_URL

APPEND_SLASH = True
SESSION_COOKIE_AGE = 3600

if RUN_ENV == 'dev':
    try:
        from config.dev import *
    except ImportError:
        pass

if RUN_ENV == 'test':
    try:
        from config.test import *
    except ImportError:
        pass

if RUN_ENV == 'deploy':
    try:
        from config.deploy import *
    except ImportError:
        pass

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : '%(levelname)s [%(asctime)s] [%(name)s:%(module)s:%(funcName)s:%(lineno)s] [%(exc_info)s] %(message)s',
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename':os.path.join(ROOT_DIR+'/logs/','access.log'),
            'formatter': 'standard'
            },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console','file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'sharefile': {
            'handlers': ['console','file','mail_admins' ],
            'level': 'DEBUG',
        },
        'kx': {
            'handlers': ['console','file','mail_admins' ],
            'level': 'DEBUG',
        }
    }
}

