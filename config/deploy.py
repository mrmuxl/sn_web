#_*_coding:utf-8_*_
import os
import logging

DEBUG = False
TEMPLATE_DEBUG = DEBUG
#django-compresshtml
COMPRESS_HTML = True

try:
    from common import *
except ImportError:
    pass

STATIC_ROOT = os.path.join(ROOT_DIR,'static')
STATIC_URL = 'http://static.simplenect.cn/' 
MEDIA_ROOT = '/data/webapp_root/upload/'
MEDIA_URL = 'http://img.simplenect.cn/'
PUBLISH_UPLOAD = '/data/webapp_root/publish/'
SERVER_LOG = '/data/admin/udtserver/'

#django_compressor
COMPRESS_ENABLED = True
COMPRESS_ROOT=STATIC_ROOT + THEME
COMPRESS_URL= STATIC_URL
COMPRESS_OUTPUT_DIR='cache'
COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.SlimItFilter']

#email
#EMAIL_HOST = 'smtp.mailgun.org'
#EMAIL_PORT = 25
#EMAIL_HOST_USER ='postmaster@simplenect.com'
#EMAIL_HOST_PASSWORD = '2tuexhqw24h2'
#EMAIL_BACKEND ='apps.backends.esmtp.EmailBackend'


EMAIL_HOST = 'smtpcloud.sohu.com'
EMAIL_PORT = 25
EMAIL_HOST_USER ='postmaster@noreplay.sendcloud.org'
EMAIL_HOST_PASSWORD = 'lk6LZFgM'


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
    'django.core.context_processors.request',
    'apps.kx.context_processors.kx_settings',
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
    'compressor.finders.CompressorFinder',
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
    'apps.http.http.SetRemoteAddrFromForwardedFor',
    'django.middleware.transaction.TransactionMiddleware',
        # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'compresshtml.middleware.CompressHtmlMiddleware',
    'pagination.middleware.PaginationMiddleware',

)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'kx',                      # Or path to database file if using sqlite3.
        'USER': 'dba_kx',                      # Not used with sqlite3.
        'PASSWORD': 'QJGNPT',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
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
    'apps.kx',
    'apps.blog',
    'apps.sharefile',
    'apps.online_user',
    'apps.auth',
    'compressor',
    'apps.client',
    'apps.ad',
    'apps.msg_board',
    'apps.bug_report',
    'apps.vipuser',
    'apps.publish',
    'apps.alipay',
    'apps.spool',
    'apps.forum',
    'apps.wmd',
    'pagination',
    'apps.group',
    'apps.filter'
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
        "LOCATION": "127.0.0.1:6383:15",
        "OPTIONS": {
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
        }
    }
}

REDIS_IP = "127.0.0.1"
REDIS_PORT = "6383"
REDIS_DB_ONLINE_USER = "0"
