from django.db import models
from django.contrib.auth import get_user_model 

from courses.models import CourseDate 

User = get_user_model()

class Transaction(models.Model):
    course_date = models.ForeignKey(
        CourseDate,
        on_delete=models.CASCADE
    )
    payor = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    amount = models.FloatField()

    created = models.DateTimeField()


    
