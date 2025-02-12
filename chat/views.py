from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from accounts.models import User

class UserChatsListView(APIView):
    """
      دریافت لیست چت‌های کاربر.

    نکات:
    1. فقط چت‌هایی که کاربر در آن‌ها عضو است نمایش داده می‌شوند.
    2. امکان جستجو بر اساس نام کاربری یکی از طرفین چت وجود دارد.
    3. چت‌ها به‌صورت پیش‌فرض بر اساس تاریخ ایجاد مرتب‌سازی می‌شوند.
    4. قابلیت صفحه‌بندی برای نمایش تعداد مشخصی از چت‌ها در هر درخواست وجود دارد.

    نمونه درخواست:
    ```
    GET /api/chat/user-chats/?search=johndoe
    ```
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user1', 'user2']
    ordering_fields = ['created_at', 'user1', 'user2']
    ordering = ['-created_at']
    
    def get(self, request):
        user = request.user
        chats = Chat.objects.filter(user1=user) | Chat.objects.filter(user2=user)
        search_query = request.query_params.get('search', None)
        if search_query:
            chats = chats.filter(
                Q(user1__username__icontains=search_query) |
                Q(user2__username__icontains=search_query) 
            )

            paginator = PageNumberPagination()
            paginator.page_size = 10
            paginated_chats = paginator.paginate_queryset(chats, request)    
            
            
        serializer = ChatSerializer(paginated_chats, many=True, context={'request': request})  
        return paginator.get_paginated_response(serializer.data)
    
class UserChatDetailView(APIView):
    
    """
    دریافت پیام‌های یک چت بین دو کاربر خاص.

    نکات:
    1. در این درخواست، کاربر باید نام کاربری طرف مقابل چت را ارسال کند.
    2. در صورت یافت نشدن کاربر، خطای 404 برمی‌گردد.
    3. پیام‌ها از چت‌های موجود بین کاربر درخواست‌دهنده و کاربر هدف بازیابی می‌شوند.
    4. پیام‌ها به‌صورت پیش‌فرض در ترتیب زمان دریافت شده نمایش داده می‌شوند.

    نمونه درخواست:
    ```
    POST /api/chat/user-chat-detail/
    {
        "username": "janedoe"
    }
    ```
    """
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
