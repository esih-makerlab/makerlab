from django.urls import path

from . import views

urlpatterns = [
    path('payement', views.course_payement, name='coupon_payement'),
]

