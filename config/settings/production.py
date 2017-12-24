import os
import environ
from .base import *

env = environ.Env()
env_file = str(BASE_DIR.path('.env'))
env.read_env(env_file)

SECRET_KEY = env('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'loldb',
    'USER': 'loldb',
    'PASSWORD': env('DB_PASSWORD'),
    'HOST': 'localhost',
    'PORT': '',
  }
}

STATIC_ROOT = env('STATIC_ROOT')
