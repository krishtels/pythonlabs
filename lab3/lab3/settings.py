"""
Django settings for lab3 project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

import django_heroku

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-7eq534u9*dqfan^m4=c(4h46jn4*%gy3xq6dsfqxkb48j(**k=')
# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = bool(os.environ.get('DJANGO_DEBUG', True))

DEBUG = True
# 'DJANGO_ALLOWED_HOSTS' должен быть в виде одной строки с хостами разделенными символом пробела
# Для примера: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'
if os.environ.get("DJANGO_ALLOWED_HOSTS"):
    ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
else:
    ALLOWED_HOSTS = ['https://lab3journal.herokuapp.com/']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'people',
    'diary',
    'mailing',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lab3.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'lab3.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", 'django.db.backends.postgresql_psycopg2'),
        "NAME": os.environ.get("SQL_DATABASE", 'diary'),
        "USER": os.environ.get("SQL_USER", "user_name"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'main_format': {
            'format': '[{asctime} - {levelname} - {module} - {filename}] {message}',
            'style': '{'
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'main_format',
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'main_format',
            'filename': 'information.log'
        }
    },

    'loggers': {
        'main': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        }

    },

}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

TEACHER = 'teacher'
STUDENT = 'student'
USER_STATUS_CHOICES = [(TEACHER, 'Учитель'), (STUDENT, 'Студент')]
SCORE_CHOICES = [(10, '10'), (9, '9'), (8, '8'), (7, '7'), (6, '6'), (5, '5'), (4, '4'), (3, '3'), (2, '2'), (1, '1')]
GENDER_CHOICES = [('М', 'М'), ('Ж', 'Ж')]

AUTH_USER_MODEL = 'people.User'

STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'diary/static/media')
IMAGES_DIR = os.path.join(MEDIA_ROOT, 'images')

if not os.path.exists(MEDIA_ROOT) or not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'login'

# REDIS settings
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'

# CELERY settings
CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_BROKER_TRANSPORT_OPTION = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

django_heroku.settings(locals())