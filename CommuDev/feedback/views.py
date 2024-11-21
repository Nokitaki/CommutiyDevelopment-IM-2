
#feedback/views.py
from django.urls import reverse_lazy
from django.views import generic
from .models import Feedback
from .forms import FeedbackForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

@login_required
def feedback_list(request):
    feedbacks = Feedback.objects.filter(user=request.user)
    return render(request, 'feedback/list.html', {'feedbacks': feedbacks})

@login_required
def feedback_create(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user  # Set the user before saving
            feedback.save()
            return redirect('feedback-list')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/create.html', {'form': form})

@login_required
def feedback_update(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk, user=request.user)
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            return redirect('feedback-list')
    else:
        form = FeedbackForm(instance=feedback)
    return render(request, 'feedback/edit.html', {'form': form})

@login_required
def feedback_delete(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk, user=request.user)
    if request.method == 'POST':
        feedback.delete()
        return redirect('feedback-list')
    return render(request, 'feedback/confirm_delete.html', {'feedback': feedback})
