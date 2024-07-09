# main/routing.py
from django.urls import path
from . import consumers
from .consumers import IssueConsumer

websocket_urlpatterns = [
    path('ws/issues/', consumers.IssueConsumer.as_asgi()),
]
