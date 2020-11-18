from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('home',views.home, name='home'),
    path('about/', views.about, name='about'),
    path('profile/', views.dashboard, name='profile'),
    path('change_language/',views.change_language,name='change_language'),
]