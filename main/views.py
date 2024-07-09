# main/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from .models import Issue, Feedback, Profile
from .forms import FeedbackForm

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

def issues(request):
    issues = Issue.objects.all() 
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            issue_id = request.POST.get('issue_id')
            issue = Issue.objects.get(id=issue_id)
            Feedback.objects.create(issue=issue, content=content, user=request.user if request.user.is_authenticated else None)
            return redirect('issues')  # Redirect to avoid form resubmission on refresh
    else:
        form = FeedbackForm()

    return render(request, 'issue_list.html', {'issues': issues, 'form': form})

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