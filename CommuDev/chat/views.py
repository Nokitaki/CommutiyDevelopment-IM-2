from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .models import Message
from .forms import MessageForm, MessageUpdateForm

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('message_list')
    else:
        form = MessageForm()
    return render(request, 'chat/send_message.html', {'form': form})

@login_required
def edit_message(request, pk):
    message = get_object_or_404(Message, pk=pk, sender=request.user)
    if request.method == 'POST':
        form = MessageUpdateForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('message_list')
    else:
        form = MessageUpdateForm(instance=message)
    return render(request, 'chat/edit_message.html', {'form': form})

@login_required
def delete_message(request, pk):
    message = get_object_or_404(Message, pk=pk, sender=request.user)
    if request.method == 'POST':
        message.delete()
        return redirect('message_list')
    return render(request, 'chat/delete_message.html', {'message': message})

class MessageListView(ListView):
    model = Message
    template_name = 'chat/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        # Show messages sent or received by the logged-in user
        return Message.objects.filter(sender=self.request.user) | Message.objects.filter(recipient=self.request.user)
