#_*_coding:utf-8_*_
import os
import logging

DEBUG = True
TEMPLATE_DEBUG = DEBUG

try:
    from kx.settings import *
except ImportError:
    pass

STATIC_ROOT = os.path.join(ROOT_DIR,'static')
STATIC_URL = '/static' + THEME
MEDIA_ROOT = os.path.join(ROOT_DIR,'media/upload/')
MEDIA_URL = '/'
PUBLISH_UPLOAD = os.path.join(ROOT_DIR,'media/upload/')
SERVER_LOG =''

EMAIL_HOST = 'mail.simplenect.cn'
EMAIL_PORT = 25
EMAIL_HOST_USER ='noreply@simplenect.cn'
EMAIL_HOST_PASSWORD = 'o86w9OQUTPW1'
EMAIL_BACKEND ='kx.backends.esmtp.EmailBackend'

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
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"


# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
# Additional locations of static files

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'http.http.SetRemoteAddrFromForwardedFor',
    'django.middleware.transaction.TransactionMiddleware',
        # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'kx',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'mrmuxl',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    }
}



INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    #'django.contrib.comments',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'gunicorn',
    'kx',
    'sharefile',
    'online_user',
    'auth',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        #'rest_framework.authentication.BasicAuthentication',
        #'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}

CACHES = {
    "default": {
        "BACKEND": "redis_cache.cache.RedisCache",
        "LOCATION": "192.168.18.200:6383:0",
        "OPTIONS": {
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
        }
    }
}

