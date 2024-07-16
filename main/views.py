# main/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Issue, Feedback, Profile
from .forms import FeedbackForm, ProgressReportForm
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import default_storage

# View for the home page
def index(request):
    return render(request, 'index.html')

# View for the about page
def about(request):
    return render(request, 'about.html')

# View for the emergency contacts page
def emergency(request):
    return render(request, 'emergency.html')

# View for submitting an issue
@login_required
def submit_issue(request):
    if request.method == 'POST':
        issue = request.POST.get('issue')
        ward = request.POST.get('ward')
        category = request.POST.get('category')
        image_option = request.POST.get('imageOption')
        image = request.FILES.get('image') if image_option == 'upload' else None
        address = request.POST.get('address')

        new_issue = Issue(issue=issue, ward=ward, category=category, image=image, address=address, reported_by=request.user)
        new_issue.save()
        return render(request, 'form_success.html', {'issue': issue, 'ward': ward})
    return render(request, 'form.html')


# View for the admin login page
def admin_login(request):
   return render(request, 'admin/admin.html')

# View for displaying the list of issues and handling feedback submission
@login_required
def issues(request):
    issues = Issue.objects.filter(reported_by=request.user)  # Filter issues by the logged-in user
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            issue_id = request.POST.get('issue_id')
            issue = Issue.objects.get(id=issue_id)
            Feedback.objects.create(issue=issue, content=content, user=request.user)
            return redirect('issues')  # Redirect to avoid form resubmission on refresh
    else:
        form = FeedbackForm()

    return render(request, 'issue_list.html', {'issues': issues, 'form': form})

# View for handling user login
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('submit_issue')  # Redirect to the issue reporting page after successful login
        else:
            # If authentication fails, re-render the login page with an error message
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    # For GET requests, render the login page
    return render(request, 'login.html')

# View for handling user signup
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        ward = request.POST.get('ward')
        
        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already taken'}, status=400)
        
        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        if user:
            profile = Profile.objects.create(user=user, phone=phone, ward=ward)
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return JsonResponse({'message': 'Signup successful'})
            return JsonResponse({'error': 'Authentication failed'}, status=400)
        return JsonResponse({'error': 'Signup failed'}, status=400)
    return render(request, 'signup.html')

# View for handling user logout
def logout_view(request):
    auth_logout(request)
    return redirect('index')  # Redirect to the home page after logout

# View for handling the progress report form
@login_required
def progress_report(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    if request.method == 'POST' and request.user.is_staff:
        form = ProgressReportForm(request.POST)
        if form.is_valid():
            progress_report = form.cleaned_data['progress_report']
            status = form.cleaned_data['status']
            address = form.cleaned_data.get('address', issue.address)
            issue.status = status
            issue.progress_report = progress_report
            issue.address = address
            issue.save()

            send_mail(
                'Issue Progress and Status Updated',
                f'Hello {issue.reported_by.username},\n\nYour issue "{issue.issue}" has been updated.\n\nStatus: {status}\nProgress Report: {progress_report}\n\nBest regards,\nTalking Box Support Team',
                settings.DEFAULT_FROM_EMAIL,
                [issue.reported_by.email],
                fail_silently=False,
            )
            return redirect('issues')
    else:
        form = ProgressReportForm(initial={'status': issue.status, 'progress_report': issue.progress_report, 'address': issue.address})

    return render(request, 'progress_report.html', {'issue': issue, 'form': form})

def list_issues(request):
    issues = Issue.objects.all()
    category_filter = request.GET.get('category')
    if category_filter:
        issues = issues.filter(category=category_filter)

    return render(request, 'list_issues.html', {'issues': issues})