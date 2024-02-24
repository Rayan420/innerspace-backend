from .base import *

DEBUG = True

<<<<<<< HEAD
ALLOWED_HOSTS = ['*']
=======
ALLOWED_HOSTS = []
>>>>>>> 90c7574b221f7e305503013034a299715768effa

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
