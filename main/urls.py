# main/urls.py
from django.urls import path
# from .views import index, about, emergency, submit_issue, admin_login, issues, login, signup
from django.conf import settings
from django.conf.urls.static import static
from . import views
from main.consumers import IssueConsumer

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('emergency/', views.emergency, name='emergency'),
    path('submit_issue/', views.submit_issue, name='submit_issue'),
    path('adminlogin/', views.admin_login, name='adminlogin'),
    path('issues/', views.issues, name='issues'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:  # Serve media files only in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)