from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()


class Resume(models.Model):
    class Meta:
        verbose_name_plural = "resumes"

    user = models.OneToOneField(to=User, on_delete=models.CASCADE,related_name='user')

    resume = models.TextField(max_length=3000, blank=True, null=True, verbose_name=_("resume"), help_text=_("Short profile's description"))

    website = models.URLField(max_length=300, blank=True, null=True, verbose_name=_("website"))

    skill_summary = models.TextField(max_length=1000, blank=True, null=True, verbose_name=_("summary of skills"))
    experience_summary = models.TextField(max_length=1000, blank=True, null=True, verbose_name=_("summary of experience"))
    training_summary = models.TextField(max_length=1000, blank=True, null=True, verbose_name=_("summary of trainings"))
    project_summary = models.TextField(max_length=1000, blank=True, null=True, verbose_name=_("summary of projects"))

    hobbies = models.TextField(max_length=1000, blank=True, null=True, verbose_name=_("hobbies"))
    tags = ArrayField(verbose_name=_('Tags'),base_field=models.TextField(),blank=True,help_text=_('Ex: electronics'),null=True)

    stackoverflow = models.URLField(blank=True, null=True, verbose_name=_("StackOverflow link"))
    github = models.URLField(max_length=300, blank=True, null=True, verbose_name=_("GitHub link"))
    linkedin = models.URLField(max_length=100, blank=True, null=True, verbose_name=_("LinkedIn link"))
    twitter = models.URLField(max_length=100, blank=True, null=True, verbose_name=_("Twitter link"))
    instagram = models.URLField(max_length=100, blank=True, null=True, verbose_name=_("instagram link"))
    facebook = models.URLField(max_length=100, blank=True, null=True, verbose_name=_("facebook link"))

