from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Chat
from .serializers import ChatSerializer

class UserChatsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        chats = Chat.objects.filter(user1=user) | Chat.objects.filter(user2=user)
        serializer = ChatSerializer(chats, many=True, context={'request': request})  # اضافه کردن request به context
        return Response(serializer.data, status=200)
    
