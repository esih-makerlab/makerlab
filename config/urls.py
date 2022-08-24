"""dj_boilerplate URL Configuration
"""
from cgitb import handler
from django.contrib import admin
from django.urls import path, include

from . import settings

from django.conf.urls.i18n import i18n_patterns

from django.conf.urls.static import static

from makerlab.moncash import views as moncash_views
from makerlab.pages import views as error_views

urlpatterns = i18n_patterns(
    path('', include('makerlab.pages.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('makerlab.account.urls')),
    path('moncash/', include('makerlab.moncash.urls')),
    path('coupon/', include('makerlab.coupon.urls')),
    path('courses/', include('makerlab.courses.urls')),
    # path('resume/', include('makerlab.resume.urls')),
    path('payement-error/', moncash_views.course_payement, name="payement"),
    # ERROR_VIEW_PATH
    path('403/', error_views.error403, name="403"),
    path('404/', error_views.error404, name="404"),
    path('500/', error_views.error500, name="500"),
    prefix_default_language=True,
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'makerlab.pages.views.error403'
handler404 = 'makerlab.pages.views.error404'
handler500 = 'makerlab.pages.views.error500'