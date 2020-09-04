from django.urls import path
from account import views
urlpatterns = [
    path('signup/', views.signUpUser, name='signup'),
]