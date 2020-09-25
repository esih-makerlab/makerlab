from django.contrib import admin
from .models import Courses,Attendee
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

# Register your models here.
class CoursesAdmin(admin.ModelAdmin,DynamicArrayMixin):
    list_display = ('id','title','teacher','price','date',)
    list_display_links = ('id',)
    list_filter = ('teacher__username',)
    search_fields = ('title','description',)
    list_per_page = 25
    autocomplete_fields = ['teacher','requirements']

class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('id','course','attendee','score','complete',)
    list_display_links = ('id',)
    list_filter = ('score','complete')
    search_fields = ('attendee__username','course__title',)
    list_per_page = 25
    autocomplete_fields = ['course','attendee']

admin.site.register(Attendee, AttendeeAdmin)
admin.site.register(Courses, CoursesAdmin)