from django.urls import path, include
from . import views

urlpatterns = [
   # https://github.com/django/django/blob/stable/3.0.x/django/contrib/auth/urls.py
   path('login/', views.user_login, name='login'),
   path('register/', views.register, name='register')
]