# main/models.py

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from dirtyfields import DirtyFieldsMixin

# Profile model to store additional information about the user
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one relationship with the User model
    phone = models.CharField(
        max_length=17,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )]
    )  # Phone number of the user with country code
    ward = models.CharField(max_length=50)  # Ward information of the user

    def __str__(self):
        return self.user.username  # Return the username of the associated user

# Signal handlers to create and save user profiles
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Issue model to store information about reported issues
class Issue(DirtyFieldsMixin, models.Model):
    PENDING = 'Pending'
    IN_PROGRESS = 'In Progress'
    RESOLVED = 'Resolved'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (RESOLVED, 'Resolved'),
    ]

    HEALTH = 'Health'
    WATER_SANITATION = 'Water & Sanitation'
    FIRES = 'Fires'
    CHILDREN_MINORS = 'Children & Minors'
    ELECTRICITY_POWER = 'Electricity & Power'
    CRIMINAL_ACTIVITIES = 'Criminal Activities'
    ROADS_INFRASTRUCTURE = 'Roads & Infrastructure'
    CATEGORY_CHOICES = [
        (HEALTH, 'Health'),
        (WATER_SANITATION, 'Water & Sanitation'),
        (FIRES, 'Fires'),
        (CHILDREN_MINORS, 'Children & Minors'),
        (ELECTRICITY_POWER, 'Electricity & Power'),
        (CRIMINAL_ACTIVITIES, 'Criminal Activities'),
        (ROADS_INFRASTRUCTURE, 'Roads & Infrastructure'),
    ]

    issue = models.TextField()  # Description of the issue
    image = models.ImageField(upload_to='issue_images/', blank=True, null=True)  # Image associated with the issue
    ward = models.CharField(max_length=100)  # Ward where the issue is located
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)  # Status of the issue
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # User who reported the issue
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the issue was created
    address = models.TextField(blank=True, null=True)  # Address of the issue location
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=HEALTH)  # Category of the issue
    progress_report = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.category}: {self.issue}'  # Return the issue description with category

# Feedback model to store feedback related to issues
class Feedback(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='feedbacks')  # Foreign key to the Issue model
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # User who provided the feedback
    content = models.TextField()  # Content of the feedback
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the feedback was created

    def __str__(self):
        return f'Feedback from {self.user.username} on issue {self.issue.issue}'  # Return a string representation of the feedback
