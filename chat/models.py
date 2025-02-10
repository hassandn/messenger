from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError

# Create your models here.
class Chat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1',unique=True)
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2',unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user1} - {self.user2}'
    
    def get_other_user(self, user):
        return self.user2 if self.user1 == user else self.user1
    


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)  # آیا پیام خوانده شده است یا نه

    def __str__(self):
        return f"Message from {self.sender.username}: {self.content[:20]}"

    def get_receiver(self):
        """تشخیص گیرنده پیام از روی چت"""
        return self.chat.get_other_user(self.sender)

    def clean(self):
        # چک می‌کنیم که ارسال‌کننده جزو کاربران چت باشد
        if self.sender not in [self.chat.user1, self.chat.user2]:
            raise ValidationError("Sender must be part of the chat")

    def save(self, *args, **kwargs):
        # قبل از ذخیره پیام، از متد clean استفاده می‌کنیم
        self.clean()
        super().save(*args, **kwargs)