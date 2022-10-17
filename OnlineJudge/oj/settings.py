"""
Django settings for oj project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
import os
import sys
import raven
from copy import deepcopy
from utils.shortcuts import get_env

production_env = get_env("OJ_ENV", "dev") == "production"

if production_env:
    from .production_settings import *
else:
    from .dev_settings import *

with open(os.path.join(DATA_DIR, "config", "secret.key"), "r") as f:
    SECRET_KEY = f.read()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Applications
VENDOR_APPS = [
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_dramatiq',
    'django_dbconn_retry',
]

if production_env:
    VENDOR_APPS.append('raven.contrib.django.raven_compat')


LOCAL_APPS = [
    'account',
    'announcement',
    'conf',
    'problem',
    'contest',
    'utils',
    'submission',
    'options',
    'judge',
]

INSTALLED_APPS = VENDOR_APPS + LOCAL_APPS

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'account.middleware.APITokenAuthMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # 'account.middleware.AdminRoleRequiredMiddleware',
    'account.middleware.SessionRecordMiddleware',
    'account.middleware.LogSqlMiddleware',
)


ROOT_URLCONF = 'oj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'oj.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/public/'

AUTH_USER_MODEL = 'account.User'

TEST_CASE_DIR = os.path.join(DATA_DIR, "test_case")
LOG_PATH = os.path.join(DATA_DIR, "log")

AVATAR_URI_PREFIX = "/public/avatar"
AVATAR_UPLOAD_DIR = f"{DATA_DIR}{AVATAR_URI_PREFIX}"

UPLOAD_PREFIX = "/public/upload"
UPLOAD_DIR = f"{DATA_DIR}{UPLOAD_PREFIX}"

STATICFILES_DIRS = [os.path.join(DATA_DIR, "public")]


LOGGING_HANDLERS = ['console', 'sentry'] if production_env else ['console']


LOGGING = {
   'version': 1,
   'disable_existing_loggers': False,
   'formatters': {
       'standard': {
           'format': '[%(asctime)s] - [%(levelname)s] - [%(name)s:%(lineno)d]  - %(message)s',
           'datefmt': '%Y-%m-%d %H:%M:%S'
       }
   },
   'handlers': {
       'console': {
           'level': 'DEBUG',
           'class': 'logging.StreamHandler',
           'formatter': 'standard'
       },
       'sentry': {
           'level': 'ERROR',
           'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
           'formatter': 'standard'
       }
   },
   'loggers': {
       'django.request': {
           'handlers': LOGGING_HANDLERS,
           'level': 'ERROR',
           'propagate': True,
       },
       'django.db.backends': {
           'handlers': LOGGING_HANDLERS,
           'level': 'ERROR',
           'propagate': True,
       },
        'dramatiq': {
            'handlers': LOGGING_HANDLERS,
            'level': 'DEBUG',
            'propagate': False,
        },
       '': {
           'handlers': LOGGING_HANDLERS,
           'level': 'WARNING',
           'propagate': True,
       }
   },
}

REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

REDIS_URL = "redis://%s:%s" % (REDIS_CONF["host"], REDIS_CONF["port"])

def redis_config(db):
    def make_key(key, key_prefix, version):
        return key

    return {
        "BACKEND": "utils.cache.MyRedisCache",
        "LOCATION": f"{REDIS_URL}/{db}",
        "TIMEOUT": None,
        "KEY_PREFIX": "",
        "KEY_FUNCTION": make_key
    }


CACHES = {
    "default": redis_config(db=1)
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.redis.RedisBroker",
    "OPTIONS": {
        "url": f"{REDIS_URL}/4",
    },
    "MIDDLEWARE": [
        # "dramatiq.middleware.Prometheus",
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Callbacks",
        "dramatiq.middleware.Retries",
        # "django_dramatiq.middleware.AdminMiddleware",
        "django_dramatiq.middleware.DbConnectionsMiddleware"
    ]
}

DRAMATIQ_RESULT_BACKEND = {
    "BACKEND": "dramatiq.results.backends.redis.RedisBackend",
    "BACKEND_OPTIONS": {
        "url": f"{REDIS_URL}/4",
    },
    "MIDDLEWARE_OPTIONS": {
        "result_ttl": None
    }
}

RAVEN_CONFIG = {
    'dsn': 'https://b200023b8aed4d708fb593c5e0a6ad3d:1fddaba168f84fcf97e0d549faaeaff0@sentry.io/263057'
}

IP_HEADER = "HTTP_X_REAL_IP"

DEFAULT_AUTO_FIELD='django.db.models.AutoField'