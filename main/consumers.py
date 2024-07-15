# main/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Issue
from twilio.rest import Client
from django.conf import settings
from .utils import send_sms

class IssueConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'issue_updates',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'issue_updates',
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        issue_id = text_data_json['issue_id']
        new_status = text_data_json['status']
        progress_report = text_data_json.get('progress_report', '')

        # Update the issue status in the database
        issue = Issue.objects.get(id=issue_id)
        issue.status = new_status
        issue.save()

        # Notify WebSocket clients
        await self.channel_layer.group_send(
            'issue_updates',
            {
                'type': 'issue_status_update',
                'issue_id': issue_id,
                'status': new_status,
                'progress_report': progress_report
            }
        )

    async def issue_status_update(self, event):
        issue_id = event['issue_id']
        new_status = event['status']
        progress_report = event.get('progress_report', '')

        await self.send(text_data=json.dumps({
            'issue_id': issue_id,
            'status': new_status,
            'progress_report': progress_report,
            'address': address,
        }))