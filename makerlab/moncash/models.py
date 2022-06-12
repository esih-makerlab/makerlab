from django.db import models
from django.contrib.auth import get_user_model 
from django.utils.timezone import now
from makerlab.courses.models import Attendee

import uuid
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class CourseTransaction(models.Model):

    class Status(models.TextChoices):
        PENDING = 'PENDING', _("Pending")
        COMPLETE = 'COMPLETE', _("Complete")

    payor = models.ForeignKey(
        Attendee,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    status = models.CharField(_('status'),max_length=25,choices=Status.choices,default=Status.PENDING,blank=False)
    created = models.DateTimeField(default=now)