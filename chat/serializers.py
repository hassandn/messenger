from rest_framework import serializers
from .models import Chat

class ChatSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ["id", "other_user", "created_at"]

    def get_other_user(self, obj):
        request_user = self.context["request"].user
        return obj.user2.username if obj.user1 == request_user else obj.user1.username
