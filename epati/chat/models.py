from datetime import datetime, timezone
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Thread(models.Model):
    first_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_user')
    second_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_second_user')

    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.now()
        self.updated = datetime.now()
        return super(Thread, self).save(*args, **kwargs)


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)