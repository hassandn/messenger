from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError


class Chat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user1} - {self.user2}"

    def get_other_user(self, user):
        return self.user2 if self.user1 == user else self.user1

    @classmethod
    def get_or_create_chat(cls, user1, user2):
        chat = cls.objects.filter(
            (models.Q(user1=user1) & models.Q(user2=user2))
            | (models.Q(user1=user2) & models.Q(user2=user1))
        ).first()

        if not chat:
            chat = cls.objects.create(user1=user1, user2=user2)

        return chat


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username}: {self.content[:20]}"

    def get_receiver(self):
        return self.chat.get_other_user(self.sender)

    def clean(self):
        if self.sender not in [self.chat.user1, self.chat.user2]:
            raise ValidationError("Sender must be part of the chat")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
