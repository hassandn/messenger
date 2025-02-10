from rest_framework import serializers
from .models import Chat, Message

class ChatSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ["id", "other_user", "created_at"]

    def get_other_user(self, obj):
        request_user = self.context["request"].user
        return obj.user2.username if obj.user1 == request_user else obj.user1.username

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()  # یا می‌توانید این را به `UserSerializer` تغییر دهید
    receiver = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'created_at', 'updated_at', 'is_read']

    def get_receiver(self, obj):
        # از متد get_receiver برای دریافت گیرنده استفاده می‌کنیم
        return obj.get_receiver().username

