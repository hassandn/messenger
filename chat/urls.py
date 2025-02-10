from django.urls import path
from .views import UserChatsListView, UserChatDetailView,CreateChatView

urlpatterns = [
    path('chats/', UserChatsListView.as_view(), name='user_chats'),
    path('chat/', UserChatDetailView.as_view(), name='user_chat'),
    path('create/', CreateChatView.as_view(), name='create_chat'),
]
