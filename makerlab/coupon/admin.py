from django.contrib import admin
from .models import CouponTransaction

# Register your models here.
class CouponTransactionAdmin(admin.ModelAdmin):
    list_display = ('id','courseDate','payor','status','created')
    list_display_links = ('id',)
    list_filter = ('status',)
    search_fields = ('payor__first_name','payor__last_name',)
    list_per_page = 25
    autocomplete_fields = ['courseDate','payor']


admin.site.register(CouponTransaction, CouponTransactionAdmin)