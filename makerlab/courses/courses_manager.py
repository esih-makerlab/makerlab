from django.db import models
from django.utils import timezone

class CourseDateManager(models.Manager):
    def all_from_now(self):
        return super(CourseDateManager, self).all().filter(date__gte=timezone.now())