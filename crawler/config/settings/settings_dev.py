import logging

from config.settings.settings import *

logger = logging.getLogger()
logger.info(LANGUAGE_CODE, TIME_ZONE)

ALLOWED_HOSTS = ["kor", "usa", "localhost", "127.0.0.1", "0.0.0.0"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'stock',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'postgres',
        'PORT': '5432',
    }
}
