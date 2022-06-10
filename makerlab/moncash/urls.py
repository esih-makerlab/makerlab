from django.urls import path

from . import views

urlpatterns = [
    path('<int:id>', views.CourseProceed, name='courseProceed'),
    
    #path('payement/', views.course_payement, name='payement'),
]

