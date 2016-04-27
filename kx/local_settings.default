#_*_coding:utf-8_*_
import os
import logging
ROOT_DIR = os.path.dirname(__file__)
THEME = '/default/'

STATIC_ROOT = os.path.join(ROOT_DIR,'static')
STATIC_URL = '/static' + THEME
MEDIA_ROOT = os.path.join(ROOT_DIR,'media/upload')
MEDIA_URL = '/'

STATICFILES_DIRS = (
	os.path.join(ROOT_DIR,'static' + THEME),
)
AUTH_USER_MODEL = 'kx.KxUser'
PASSWORD_HASHERS = (
'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
)

TEMPLATE_DIRS = (
    os.path.join(ROOT_DIR,'templates' + THEME),
)

TEMPLATE_CONTEXT_PROCESSORS =(
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
)

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
        'kx': {
            'handlers': ['console','file','mail_admins' ],
            'level': 'DEBUG',
        }
    }
}

EMAIL = 'mrmuxl@sina.com'
ADMINS = (
    ('admin', EMAIL),
)
