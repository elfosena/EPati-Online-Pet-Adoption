from django.urls import path
from . import views

app_name = 'chat'
urlpatterns = [
    path('', views.ChatLobbyView.as_view(), name='chat_lobby'),
    path('thread', views.ChatThreadView.as_view(), name='thread'),
]