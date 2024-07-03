# main/views.py
from django.shortcuts import render, redirect
from .models import Issue


def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def emergency(request):
    return render(request, 'emergency.html')

def submit_issue(request):
    if request.method == 'POST':
        issue = request.POST.get('issue')
        ward = request.POST.get('ward')
        image_option = request.POST.get('imageOption')
        image = request.FILES.get('image') if image_option == 'upload' else None
        
        new_issue = Issue(issue=issue, ward=ward, image=image)
        new_issue.save()
        return render(request, 'form_success.html', {'issue': issue, 'ward': ward})
    return render(request, 'form.html')

def admin_login(request):
    return render(request, 'admin/admin.html')
