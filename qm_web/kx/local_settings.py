


import os
ROOT_DIR = os.path.dirname(__file__)
THEME = '/default/'

STATIC_ROOT = os.path.join(ROOT_DIR,'static')
STATIC_URL = '/static' + THEME
MEDIA_ROOT = os.path.join(ROOT_DIR,'media')
MEDIA_URL = '/media/'

STATICFILES_DIRS = (
	os.path.join(ROOT_DIR,'static' + THEME),
)
#AUTH_USER_MODEL = 'kx.KxUser'

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

EMAIL = 'mrmuxl@sina.com'
ADMINS = (
    ('admin', EMAIL),
)
