from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='courses_home'),
    path('detail/<int:id>', views.course_details, name='course_detail'),
    path('enroll', views.course_enrollement, name='enroll'),
    path('payement/', views.course_payement, name='payement'),
    path('search/', views.search_results, name='search_results')
]