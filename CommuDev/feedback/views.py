# views.py
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count
from django.utils import timezone
from .models import Feedback
from .forms import FeedbackForm
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test

@login_required
def feedback_list(request):
    if request.user.is_staff:
        # Staff can see all feedback
        feedbacks = Feedback.objects.all()
    else:
        # Regular users only see their own feedback
        feedbacks = Feedback.objects.filter(user=request.user)
    
    form = FeedbackForm()
    feedback_stats = _get_feedback_stats(request.user)
    
    context = {
        'feedbacks': feedbacks,
        'form': form,
        'feedback_stats': feedback_stats,
    }
    
    return render(request, 'feedback/feedback.html', context)

@login_required
def feedback_create(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            try:
                feedback = form.save(commit=False)
                feedback.user = request.user
                feedback.date_submitted = timezone.now()  # Explicitly set submission date
                feedback.save()
                messages.success(request, 'Your feedback has been submitted successfully!')
                return redirect('feedback:feedback-list')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
        else:
            # Collect form errors to display to the user
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field.capitalize()}: {error}")
            
            messages.error(request, 'Please correct the following errors:\n' + '\n'.join(error_messages))
    
    # Redirect back to the feedback list with the form
    return redirect('feedback:feedback-list')

@login_required
def feedback_edit(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feedback updated successfully!')
            return redirect('feedback:feedback-list')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    return redirect('feedback:feedback-list')

@login_required
def feedback_delete(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk, user=request.user)
    
    if request.method == 'POST':
        feedback.delete()
        messages.success(request, 'Feedback deleted successfully!')
        return redirect('feedback:feedback-list')
    
    return redirect('feedback:feedback-list')


def _get_feedback_stats(user):
    """Helper function to get feedback statistics"""
    feedbacks = Feedback.objects.filter(user=user)
    return {
        'total': feedbacks.count(),
        'pending': feedbacks.filter(status='pending').count(),
        'in_progress': feedbacks.filter(status='in_progress').count(),
        'resolved': feedbacks.filter(status='resolved').count(),
    }
    
@user_passes_test(lambda u: u.is_staff)
def update_feedback_status(request, pk):
    if request.method == 'POST':
        try:
            feedback = Feedback.objects.get(pk=pk)
            data = json.loads(request.body)
            new_status = data.get('status')
            
            if new_status in dict(Feedback.STATUS_CHOICES):
                feedback.status = new_status
                feedback.save()
                return JsonResponse({'success': True})
            
            return JsonResponse({'success': False, 'error': 'Invalid status'})
        except Feedback.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Feedback not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})