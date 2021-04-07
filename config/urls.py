"""dj_boilerplate URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

from . import settings

from django.conf.urls.i18n import i18n_patterns

from django.conf.urls.static import static

urlpatterns = i18n_patterns(
    path('', include('makerlab.pages.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('makerlab.account.urls')),
    path('moncash/', include('makerlab.moncash.urls')),
    path('coupon/', include('makerlab.coupon.urls')),
    path('courses/', include('makerlab.courses.urls')),
    path('resume/', include('makerlab.resume.urls')),
    prefix_default_language=True,
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)