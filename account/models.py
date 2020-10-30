from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

from .account_manager import UserManager

import uuid

def random_username(sender, instance, **kwargs):

    if instance.username is None:

        def get_username(next_val):

            while len(str(next_val)) < 6:
                next_val = '0'+str(next_val)

            return 'MP'+next_val

        last_username = User.objects.latest('username').username
        next_val = int(last_username.replace('MP',''))+1

        username = get_username(next_val)

        while User.objects.filter(username=username):
            username = get_username(next_val+1)

        instance.username = username

class User(AbstractUser):
    email = models.EmailField(_('email address'),help_text='Ex:john@winterfell.got', max_length=255,blank=False, unique=True)
    first_name = models.CharField(_('first name'),help_text='Ex:john', max_length=150, blank=False)
    last_name = models.CharField(_('last name'),help_text='Ex:snow', max_length=150, blank=False)
    phone =  PhoneNumberField(_('phone number'),help_text='Ex:+509XXXXXXXX',blank=True,max_length=15)
    country = CountryField(_('select country'),blank=True,help_text=_('select country'),default='HT')
    photo = models.ImageField(upload_to='account_photos', blank=True, default=None)
    username = models.CharField(_('username'),help_text='Ex:MP0001',max_length=10,default=None,unique=True)
    email_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return self.username
