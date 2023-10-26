# routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

from . import consumers
from .consumers import NotificationConsumer

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
]
