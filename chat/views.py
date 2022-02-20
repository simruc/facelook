
# Create your views here.
from concurrent.futures import thread
from django.dispatch import receiver
from django.shortcuts import render
from accounts.models import MessageModel, User, ThreadModel
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

def index(request):
    thread = ThreadModel.objects.all()
    context = {
        'thread':thread
    }
    return render(request, 'index.html', context)

def room(request, username):
    
    other_user = User.objects.get(username=username)
    me = User.objects.get(username= request.user.username)
    try:
        thread_obj = ThreadModel.objects.get(Q(user=me, receiver=other_user)|Q(user=other_user, receiver=me))
    except ObjectDoesNotExist:
        thread_obj = ThreadModel.objects.create(user=me, receiver=other_user)
    message_list = MessageModel.objects.filter(thread=thread_obj)
    return render(request, 'accounts/thread1.html', {
        'username': username,
        'message_list':message_list,
        'thread': thread_obj
    })