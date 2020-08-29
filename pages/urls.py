from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('membership/', views.membership, name='membership'),
    path('cours/', views.cours, name='cours'),
    path('about/', views.about, name='about'),
    
]