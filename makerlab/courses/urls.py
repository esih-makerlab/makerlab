from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='courses_home'),
    path('detail/<int:id>', views.course_details, name='course_detail'),
    path('attendee/<int:id>', views.get_attendee, name="get_attendee"),
    path('enroll/<int:id>', views.course_enrollement, name='enroll'),
    path('search/', views.search_results, name='search_results')
]