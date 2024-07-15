# main/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Issue, Profile
# from twilio.rest import Client
from django.conf import settings
import time
from django.db import OperationalError
from django.core.mail import send_mail

@receiver(post_save, sender=Issue)
def notify_issue_status_change(sender, instance, **kwargs):
       # Check if the status field has been updated
    if 'status' in instance.get_dirty_fields():
        print(f"Status changed for issue #{instance.id} to {instance.status}")
        
        # Check if the issue has a reporter
        if instance.reported_by is not None:
            try:
                # Notify via Email
                def send_email(to_email, subject, message):
                    send_mail(
                        subject,
                        message,
                        'hadijasuleiman@students.tukenya.ac.ke',
                        [to_email],
                        fail_silently=False,
                    )

                # Get the reporter's email and username
                email = instance.reported_by.email
                username = instance.reported_by.username

                # Send Email notification
                email_subject = "Issue Status Update"
                email_message = f"Dear {instance.reported_by.username},\n\nThe status of your issue '{instance.issue}' has been updated to '{instance.status}'.\n\nBest regards,\nTalking Box Team"
                send_email(email, email_subject, email_message)
            
            except Profile.DoesNotExist:
                print(f"User {instance.reported_by.username} does not have a profile.")
        else:
            print("Reported_by field is None.")