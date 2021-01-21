from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from .models import Resume

class ResumeAdmin(admin.ModelAdmin,DynamicArrayMixin):
    list_display = ('id','user', 'website')
    list_display_links = ('id',)
    list_filter = ('user',)
    search_fields = ('user__first_name','user__last_name','user__email',)
    list_per_page = 25
    autocomplete_fields = ['user']
    

admin.site.register(Resume, ResumeAdmin)