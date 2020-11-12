from django.db import models
from django.contrib.auth import get_user_model 
from django.utils.timezone import now
from courses.models import CourseDate 

from django.utils.translation import gettext_lazy as _

User = get_user_model()

class CourseTransaction(models.Model):

    class Status(models.TextChoices):
        PENDING = 'PENDING', _("Pending")
        COMPLETE = 'COMPLETE', _("Complete")

    courseDate = models.ForeignKey(
        CourseDate,
        on_delete=models.CASCADE
    )
    payor = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    status = models.CharField(_('status'),max_length=25,choices=Status.choices,default=Status.PENDING,blank=False)
    created = models.DateTimeField(default=now)