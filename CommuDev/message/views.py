from django.shortcuts import render

# Create your views here.

# message/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserMessage, Message
from .forms import UserMessageForm, MessageForm

@login_required
def user_message_list(request):
    try:
        user_messages = UserMessage.objects.filter(users=request.user)
    except:
        user_messages = []
    return render(request, 'message/user_message_list.html', {'user_messages': user_messages})

@login_required
def user_message_create(request):
   if request.method == 'POST':
       form = UserMessageForm(request.POST)
       if form.is_valid():
           user_message = form.save()
           return redirect('message_create', user_message_id=user_message.id)
   else:
       form = UserMessageForm()
   return render(request, 'message/user_message_form.html', {'form': form})

@login_required
def message_create(request, user_message_id):
   user_message = get_object_or_404(UserMessage, id=user_message_id)
   if request.method == 'POST':
       form = MessageForm(request.POST)
       if form.is_valid():
           message = form.save(commit=False)
           message.user_message = user_message
           message.save()
           return redirect('user_message_list')
   else:
       form = MessageForm()
   return render(request, 'message/message_form.html', {'form': form, 'user_message': user_message})