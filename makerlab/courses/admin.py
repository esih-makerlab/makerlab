from django.contrib import admin
from .models import Course,Attendee,CourseDate
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

# Register your models here.
class CourseAdmin(admin.ModelAdmin,DynamicArrayMixin):
    list_display = ('id','title','note','photo',)
    list_display_links = ('id',)
    list_filter = ('requirements',)
    search_fields = ('title','description','note')
    list_per_page = 25
    autocomplete_fields = ['requirements']

class CourseDateAdmin(admin.ModelAdmin):
    list_display = ('id','date','course','teacher','price','nb_attendees',)
    list_display_links = ('id',)
    list_filter = ('date','nb_attendees','teacher__email',)
    search_fields = ('nb_attendees','date',)
    list_per_page = 25
    autocomplete_fields = ['teacher','course','attendees']

class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('id','date','attendee','score','complete',)
    list_display_links = ('id',)
    list_filter = ('score','complete')
    search_fields = ('attendee__email','date__course__title',)
    list_per_page = 25
    autocomplete_fields = ['date','attendee']

admin.site.register(Attendee, AttendeeAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseDate, CourseDateAdmin)