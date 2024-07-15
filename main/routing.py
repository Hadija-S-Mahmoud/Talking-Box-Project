# main/routing.py

from django.urls import path
from . import consumers
from .consumers import IssueConsumer

# Define the WebSocket URL patterns
websocket_urlpatterns = [
    path('ws/issues/', consumers.IssueConsumer.as_asgi()),  # Route for the IssueConsumer WebSocket
]
