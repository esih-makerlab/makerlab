from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

from .account_manager import UserManager

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(_('Email '),help_text='Ex:john@winterfell.got', max_length=255,blank=False, unique=True)
    first_name = models.CharField(_('Prénom'),help_text='Ex:john', max_length=150, blank=False)
    last_name = models.CharField(_('Nom'),help_text='Ex:snow', max_length=150, blank=False)
    phone =  PhoneNumberField(_('Téléphone'),help_text='Ex:+509XXXXXXXX',blank=True,max_length=15)
    country = CountryField(_('Pays'),blank=True,help_text=_('Selectionner votre pays'),default='HT')
    photo = models.ImageField(upload_to='account_photos', blank=True, default=None)
    email_verified = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
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
        return self.get_full_name()
