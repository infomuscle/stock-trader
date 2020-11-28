from config.settings.settings import *
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