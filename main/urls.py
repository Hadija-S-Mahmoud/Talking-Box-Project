# main/urls.py

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from main.consumers import IssueConsumer
from django.contrib.auth import views as auth_views

# Define the URL patterns
urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('about/', views.about, name='about'),  # About page
    path('emergency/', views.emergency, name='emergency'),  # Emergency contacts page
    path('submit_issue/', views.submit_issue, name='submit_issue'),  # Submit issue page
    path('adminlogin/', views.admin_login, name='adminlogin'),  # Admin login page
    path('issues/', views.issues, name='issues'),  # Issues list page
    path('login/', views.login, name='login'),  # User login page
    path('signup/', views.signup, name='signup'),  # User signup page
    path('logout/', views.logout_view, name='logout'),  # User logout page
    path('progress_report/<int:issue_id>/', views.progress_report, name='view_progress_report'),
    path('list_issues/', views.list_issues, name='list_issues'),
    path('issue-analysis/', views.issue_analysis, name='issue_analysis'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Serve static files

# Serve media files only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
