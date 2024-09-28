from django.db import models
from Authentication.models import User

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    participants = models.ManyToManyField(User)
    is_private = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"
    

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username}: {self.content[:50]}'
