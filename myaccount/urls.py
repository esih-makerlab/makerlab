from django.urls import path
from myaccount import views


urlpatterns = [
    path('signup/', views.signUpUser, name='signupuser'),
]