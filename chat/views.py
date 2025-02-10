from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404
from rest_framework import status


from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from accounts.models import User
class UserChatsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        chats = Chat.objects.filter(user1=user) | Chat.objects.filter(user2=user)
        serializer = ChatSerializer(chats, many=True, context={'request': request})  
        return Response(serializer.data, status=200)
    
class UserChatDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data.get('username')
        try:
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=404)

        chats = Chat.objects.filter(
            (Q(user1=request.user) & Q(user2=target_user)) | 
            (Q(user2=request.user) & Q(user1=target_user))
        )
        
        messages = Message.objects.filter(chat__in=chats)

        serializer = MessageSerializer(messages, many=True, context={'request': request})
        return Response(serializer.data, status=200)


class CreateChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        receiver_username = request.data.get("receiver_username")
        
        if not receiver_username:
            return Response({"detail": "Receiver username is required."}, status=status.HTTP_400_BAD_REQUEST)

        sender = request.user

        receiver = get_object_or_404(User, username=receiver_username)

        chat = Chat.get_or_create_chat(sender, receiver)

        chat_serializer = ChatSerializer(chat, context={'request': request})

        return Response(chat_serializer.data, status=status.HTTP_201_CREATED)
