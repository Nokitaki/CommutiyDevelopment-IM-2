from django.conf import settings
from django.db import models

class UserMessage(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_messages')
    subject = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

class Message(models.Model):
    user_message = models.ForeignKey(UserMessage, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)