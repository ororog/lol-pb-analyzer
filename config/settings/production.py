import os
from .base import *

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'loldb',
    'USER': 'loldb',
    'PASSWORD': os.environ['DB_PASSWORD'],
    'HOST': 'localhost',
    'PORT': '',
  }
}

STATIC_ROOT = os.environ['STATIC_ROOT']
SLEEP_TIME_AFTER_CRAWLING = int(os.environ.get('SLEEP_TIME_AFTER_CRAWLING', 1))
