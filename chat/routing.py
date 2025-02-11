from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    # path(r'ws/chat/{pk}/$', ChatConsumer.as_asgi()),
    # path(r'ws/chat/', ChatConsumer.as_asgi()),
    path('ws/chat/<int:chat_id>/',ChatConsumer.as_asgi()),
    path('ws/chat/', ChatConsumer.as_asgi()),
]
