from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='courses_home'),
    path('detail', views.course_details, name='course_details'),
]