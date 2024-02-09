from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import ChatRoom, Message
# Create your views here.

@login_required
def chatrooms(request):
    chatrooms = ChatRoom.objects.all()
    return render(request, 'chatroom/index.html', {'chatrooms':chatrooms})

@login_required
def chatroom(request, slug):
    chatroom = ChatRoom.objects.get(slug=slug)
    messages = Message.objects.filter(chatroom=chatroom)[0:25]
    return render(request, 'chatroom/chatroom.html', {'chatroom':chatroom, 'messages':messages})

