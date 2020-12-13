from .settings import *

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("DB_MK_NAME"),
        'USER': env("DB_MK_USER"),
        'PASSWORD': env("DB_MK_PASSWORD"),
        'HOST': env("DB_MK_HOST"),
        'PORT': env("DB_MK_PORT"),
    }
}
