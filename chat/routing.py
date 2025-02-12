from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path("ws/chat/<int:chat_id>/", ChatConsumer.as_asgi()),
    path("ws/chat/", ChatConsumer.as_asgi()),
]
