from django.urls import path
from django.contrib.auth import views as auth_views


from myaccount import views
from myaccount.forms import LoginForm


urlpatterns = [
    path('login/', views.user_login, name='login_for_modal'),
    path('signup/', views.signUpUser, name='signupuser'),
]