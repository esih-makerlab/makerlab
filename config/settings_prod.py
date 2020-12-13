import os
from .settings import *
import django_heroku 

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# django anymail
ANYMAIL = {
    "MAILGUN_API_KEY": os.environ.get("MAILGUN_API_KEY"),
    "MAILGUN_SENDER_DOMAIN": os.environ.get("MAILGUN_SENDER_DOMAIN")
}

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")

MONCASH = {
    'CLIENT_ID' : os.environ.get('MONCASH_CLIENT_ID'),
    'SECRET_KEY': os.environ.get('MONCASH_SECRET_KEY'),
}

django_heroku.settings(locals())