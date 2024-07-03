# main/urls.py
from django.urls import path
from .views import index, about, emergency, submit_issue, admin_login

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('emergency/', emergency, name='emergency'),
    path('submit_issue/', submit_issue, name='submit_issue'),
    path('adminlogin/', admin_login, name='adminlogin'),
]
