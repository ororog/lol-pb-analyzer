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
    'NAME': env('DB_NAME'),
    'USER': env('DB_USERNAME'),
    'PASSWORD': env('DB_PASSWORD'),
    'HOST': '',
    'PORT': '',
  }
}

STATIC_ROOT = env('STATIC_ROOT')
