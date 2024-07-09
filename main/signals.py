from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Issue
from .utils import send_sms

@receiver(post_save, sender=Issue)
def notify_issue_status_change(sender, instance, **kwargs):
    if 'status' in instance.get_dirty_fields():
        if instance.reporter and hasattr(instance.reporter, 'profile'):
            phone = instance.reporter.profile.phone
            message = f"The status of your reported issue '{instance.issue}' has changed to '{instance.status}'."
            send_sms(phone, message)
