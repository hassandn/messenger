from rest_framework import serializers
from .models import User

# سریالایزر برای مدل User
class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'phone', 'profile_picture']
