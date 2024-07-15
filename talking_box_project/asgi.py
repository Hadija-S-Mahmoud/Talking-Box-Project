"""
ASGI config for talking_box_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import main.routing  # Import the routing configuration for the main app
from main.consumers import IssueConsumer  # Import the consumer for WebSocket handling
from channels.security.websocket import AllowedHostsOriginValidator
from talking_box_project import routing

# Set the default settings module for the 'talking_box_project' project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talking_box_project.settings')

# Define the ASGI application with different protocol type routers
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Route HTTP requests to the Django ASGI application
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                main.routing.websocket_urlpatterns  # Route WebSocket requests based on URL patterns defined in main.routing
            )
        )
    ),
})
