import logging

from config.settings.settings import *

logger = logging.getLogger()
logger.info(LANGUAGE_CODE, TIME_ZONE)

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
