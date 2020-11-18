from django.urls import path
from . import views

urlpatterns = [
    path('login',views.login_user,name='login'),
    path('register',views.register_user,name='register'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('profile',views.profile,name='profile'),
    path('change_password',views.change_password,name='change_password'),
    path('logout',views.logout_user,name='logout'),
    path('verify_email_request',views.verify_email_request,name='verify_email_request'),
    path('verify_email/<uidb64>/<token>',views.verify_email,name='verify_email'),
    path('reset_password_request',views.reset_password_request,name='reset_password_request'),
    path('reset_pasword/<uidb64>/<token>',views.reset_password,name='reset_password'),
]