"""dj_boilerplate URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('moncash/', include('moncash.urls')),
    path('courses/', include('courses.urls')),
]

