from django.contrib import admin

from chat.models import ChatMessage, Thread

# Register your models here.
admin.site.register(Thread)
admin.site.register(ChatMessage)

