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

MONCASH = {
    'CLIENT_ID' : env('MONCASH_CLIENT_ID'),
    'SECRET_KEY': env('MONCASH_SECRET_KEY'),
}

ANYMAIL = {
    "MAILGUN_API_KEY": env("MAILGUN_API_KEY"),
    "MAILGUN_SENDER_DOMAIN": env("MAILGUN_SENDER_DOMAIN")
}

DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")