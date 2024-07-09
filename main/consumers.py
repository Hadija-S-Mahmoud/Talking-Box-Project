# main/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Issue
from twilio.rest import Client
from django.conf import settings

class IssueConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "issue_updates",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "issue_updates",
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        issue_id = data['issue_id']
        new_status = data['status']

        issue = await Issue.objects.get(id=issue_id)
        issue.status = new_status
        await issue.save()

        # Send SMS using Twilio
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Issue {issue_id} status updated to {new_status}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to='+254716167980'
        )

        await self.channel_layer.group_send(
            "issue_updates",
            {
                'type': 'issue_update',
                'issue_id': issue_id,
                'status': new_status,
            }
        )

    async def issue_update(self, event):
        await self.send(text_data=json.dumps({
            'issue_id': event['issue_id'],
            'status': event['status']
        }))
