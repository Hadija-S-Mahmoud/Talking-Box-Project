# main/forms.py

from django import forms
from .models import Issue, Feedback
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Define a form for the Feedback model
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['content']  # Fields to include in the form
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your feedback here...'}),  # Custom widget for the content field
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email address already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken.")
        return username

class ProgressReportForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['progress_report', 'status', 'address']

