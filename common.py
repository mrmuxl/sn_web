#_*_coding:utf-8_*_

import os

# RUN_ENV = dev or test or deploy
RUN_ENV = os.getenv("RUN_ENV",default='dev')

ROOT_DIR = os.path.dirname(__file__)

EMAIL = 'mrmuxl@sina.com'
ADMINS = (
    ('admin', EMAIL),
)

DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i:s'
SHORT_DATE_FORMAT = 'Y-m-d'
SHORT_DATETIME_FORMAT = 'Y-m-d H:i:s'
MANAGERS = ADMINS

ALLOWED_HOSTS = ['zhiwo.net','localhost']

#THEME = '/default/'
THEME = '/classic/'

DOMAIN = 'http://www.zhiwo.net'
DOWNLOAD='http://download.zhiwo.net'

LOGIN_URL = '/User/login/'
LOGOUT_URL='/User/logout/'
LOGIN_REDIRECT_URL = LOGIN_URL

APPEND_SLASH = True
SESSION_COOKIE_AGE = 604800

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
            #'filters': ['require_debug_false'],
            'filename':os.path.join(ROOT_DIR+'/logs/','access.log'),
            'formatter': 'standard'
            },
        'alipay': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            #'filters': ['require_debug_false'],
            'filename':os.path.join(ROOT_DIR+'/logs/','alipay.log'),
            'formatter': 'standard'
            },
        'spool': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            #'filters': ['require_debug_false'],
            'filename':os.path.join(ROOT_DIR+'/logs/','spool.log'),
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
            'propagate': False,
        },
        'django.request': {
            'handlers': ['file','mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'apps.sharefile': {
            'handlers': ['console','file','mail_admins' ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'apps.client': {
            'handlers': ['console','file','mail_admins' ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'apps.auth': {
            'handlers': ['console','file','mail_admins' ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'apps.kx': {
            'handlers': ['console','file','mail_admins' ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'apps.accounts': {
            'handlers': ['console','file','mail_admins' ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'apps.blog': {
            'handlers': ['console','file','mail_admins' ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'apps.msg_board': {
            'handlers': ['console','file','mail_admins' ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'apps.ad': {
            'handlers': ['console','file','mail_admins' ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'apps.bug_report': {
            'handlers': ['console','file','mail_admins' ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'apps.vipuser': {
            'handlers': ['console','file','mail_admins' ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'apps.publish': {
            'handlers': ['console','file','mail_admins' ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'apps.alipay': {
            'handlers': ['console','alipay','mail_admins' ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'apps.spool': {
            'handlers': ['console','spool','mail_admins' ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'gunicorn': {
            'handlers': ['console','file' ],
            'level': 'ERROR',
            'propagate': False,
        },
         'apps.group': {
            'handlers': ['console','file','mail_admins' ],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

