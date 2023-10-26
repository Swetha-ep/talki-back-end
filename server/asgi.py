# asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Default HTTP application
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # Import your WebSocket URL routing here
        )
    ),
})
