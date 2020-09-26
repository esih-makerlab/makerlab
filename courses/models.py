from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone
from django_better_admin_arrayfield.models.fields import ArrayField

class Courses(models.Model):
    class Currencies(models.TextChoices):
        HTG = 'HTG', _("HTG")

    class Meta:
        verbose_name_plural = "courses"
    
    teacher = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(_('title'),help_text=_('Ex: c++ Introduction'), max_length=255,blank=False)
    price = models.DecimalField(_('price'),help_text=_('Ex: 12.99'),max_length=255,max_digits=11,decimal_places=2,blank=False)
    currency = models.CharField(_('currency'),max_length=25,choices=Currencies.choices,default=Currencies.HTG,blank=False)
    nb_attendees = models.IntegerField(_('number of attendees'),help_text=_('Ex: 50'),blank=False)
    date = models.DateTimeField(_('date'),max_length=255,blank=False)
    next_date = models.DateTimeField(_('next date'),max_length=255,blank=False)
    links = ArrayField(verbose_name=_('please add link'),base_field=models.URLField(),blank=True,help_text=_('Ex: https://www.site.com/something.pdf'),null=True)
    note = models.TextField(_('note'),help_text=_('some additional note'),blank=True,null=True)
    description = models.TextField(_('description'),help_text=_('some description'),blank=False)
    tags = ArrayField(verbose_name=_('please add tag'),base_field=models.TextField(),blank=True,help_text=_('Ex: Arduino'),null=True)
    requirements = models.ManyToManyField(to='self',verbose_name='requirements',blank=True)
    attendees = models.ManyToManyField(to=get_user_model(),through='Attendee',through_fields=('course','attendee'),related_name='attendees',blank=True)

    REQUIRED_FIELDS = ['title','price','currency','nb_attendees','description','teacher','date']

    def __str__(self):
        return 'TITLE:%s ID:%s' % (self.title,self.id)

class Attendee(models.Model):

    class Meta:
        verbose_name_plural = "Attendees"

    course = models.ForeignKey(verbose_name=_('course'),to=Courses, on_delete=models.CASCADE)
    attendee = models.ForeignKey(verbose_name=_('attendee'),to=get_user_model(), on_delete=models.CASCADE)
    complete = models.BooleanField(verbose_name=_('complete'),blank=False,default=False)
    score = models.DecimalField(_('score'),help_text=_('Ex: 18.5'),max_length=255,max_digits=11,decimal_places=2,blank=False,default=0)

    REQUIRED_FIELDS = ['course','attendee','score','complete']

    def __str__(self):
        return 'COURSE:%s  ATTENDEE:%s' % (self.course.id,self.attendee.id)

