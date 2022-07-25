from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from chat.models import Thread
from django.db.models import Q
from django.contrib.auth.models import User


from common.views import BaseView

# Create your views here.

class ChatLobbyView(BaseView, LoginRequiredMixin):

    def get(self, request):
        threads = Thread.objects.filter(Q(first_user=request.user) | Q(second_user=request.user)).distinct().prefetch_related('chatmessage_thread')
        self.context.update({
            'threads': threads.order_by('-updated'),
        })
        return render(request, 'chat/lobby.html', self.context)

class ChatThreadView(BaseView, LoginRequiredMixin):

    def get(self, request):
        pk = request.GET.get('id')
        other_user = get_object_or_404(User, id=pk)
        condition = (Q(first_user=request.user, second_user=other_user) | Q(first_user=other_user, second_user=request.user))

        if Thread.objects.filter(condition).exists():
            wanted_thread = get_object_or_404(Thread, condition)
        else:
            wanted_thread = Thread.objects.create(first_user=request.user, second_user=other_user)

        threads = Thread.objects.filter(Q(first_user=request.user) | Q(second_user=request.user)).distinct().prefetch_related('chatmessage_thread')
        self.context.update({
            'threads': threads.order_by('-updated'),
            'wanted_thread': wanted_thread,
        })
        return render(request, 'chat/chatbox.html', self.context)