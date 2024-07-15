# main/utils.py

from twilio.rest import Client
from django.conf import settings

def send_sms(to_phone_number, body):
    """Send an SMS notification."""
    if not to_phone_number:
        raise ValueError("The phone number must be provided")

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=body,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to_phone_number
    )
    return message
