from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import AddUserForm, UpdateUserAdminForm,Group,GroupAdminForm
from django.contrib import admin
from .models import User

# from ..resume.models import Resume

# class ResumeInline(admin.StackedInline):
#     model=Resume
#     min_num=1
#     max_num=1
#     extra=1
    
class UserAdmin(BaseUserAdmin):
    form = UpdateUserAdminForm
    add_form = AddUserForm

    list_display = ('email', 'first_name', 'last_name', 'phone', 'is_staff','email_verified')
    list_filter = ('is_staff','email_verified')
    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone','email_verified')}),
        ('Permissions', {'fields': ('is_active', 'is_staff','is_superuser','groups','user_permissions')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email', 'first_name', 'last_name', 'password1',
                    'password2'
                )
            }
        ),
    )
    search_fields = ('email', 'first_name', 'last_name', 'phone',)
    ordering = ('first_name', 'last_name')

    #inlines = [ResumeInline]

# Unregister the original Group admin.
admin.site.unregister(Group)

# Create a new Group admin.
class GroupAdmin(admin.ModelAdmin):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']

# Register the new Group ModelAdmin.
admin.site.register(Group, GroupAdmin)

admin.site.register(User, UserAdmin)
