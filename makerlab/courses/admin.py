from django.contrib import admin
from .models import Course,WhatYoullLearn,CourseSection,Attendee,CourseDate
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

# Register your models here.
class CourseAdmin(admin.ModelAdmin,DynamicArrayMixin):
    fieldsets = ((None,{'fields':('title','description','note','links','tags','photo','requirements','certification','duration')}),)
    list_display = ('id','title','note','photo','certification', 'duration')
    list_display_links = ('id',)
    list_filter = ('requirements',)
    search_fields = ('title','description','note')
    list_per_page = 25
    autocomplete_fields = ['requirements']

class WhatYoullLearnAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    list_display_links = ('id',)
    list_filter = ('title',)
    search_fields = ('title',)
    list_per_page = 25
    autocomplete_fields = ['course',]

class CourseSectionAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    list_display_links = ('id',)
    list_filter = ('title',)
    search_fields = ('title',)
    list_per_page = 25
    autocomplete_fields = ['course',]

class CourseDateAdmin(admin.ModelAdmin):
    list_display = ('id','start_date','end_date','course','teacher','price','nb_attendees',)
    list_display_links = ('id',)
    list_filter = ('start_date','nb_attendees','teacher__email',)
    search_fields = ('nb_attendees','date',)
    list_per_page = 25
    autocomplete_fields = ['teacher','course']

class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('id','start_date','first_name','last_name','telephone','email','address','score','complete')
    list_display_links = ('id',)
    list_filter = ('score','complete','last_name','telephone','email')
    search_fields = ('attendee__email','date__course__title','first_name','last_name','telephone','email')
    list_per_page = 25
    autocomplete_fields = ['start_date',]

admin.site.register(Attendee, AttendeeAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseDate, CourseDateAdmin)
admin.site.register(WhatYoullLearn, WhatYoullLearnAdmin)
admin.site.register(CourseSection, CourseSectionAdmin)