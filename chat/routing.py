from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path("chat/<int:id>/", ChatConsumer.as_asgi()),
]