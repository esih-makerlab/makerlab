from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    """
    A User Profile model. Complementary data of 'Django auth models'
    """

    class Meta:
        verbose_name_plural = 'Profiles'

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE
    )

    birthdate = models.DateField('Birthdate')
    
    biography = models.TextField('Biography', blank=True)
    
