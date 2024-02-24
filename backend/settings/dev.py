from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

SECRET_KEY = 'MY SECRET KEY'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'innerspace',
        'USER': 'root',
        'PASSWORD': '',
        'HOST':'localhost',
        'PORT':'3306',
    }
}
