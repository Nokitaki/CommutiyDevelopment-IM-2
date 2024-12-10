# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count
from django.views.decorators.http import require_http_methods
from django.core.exceptions import PermissionDenied
from .models import Feedback
from .forms import FeedbackForm
import json

@login_required
def feedback_list(request):
    """
    Display feedback list and dashboard based on user role.
    """
    context = {
        'form': FeedbackForm(),
    }

    if request.user.is_staff:
        # Admin view with full statistics
        feedbacks = Feedback.objects.all().select_related('user').order_by('-date_submitted')
        
        # Calculate statistics for admin dashboard
        context.update({
            'feedbacks': feedbacks,
            'all_feedback_stats': {
                'total': feedbacks.count(),
                'pending': feedbacks.filter(status='pending').count(),
                'in_progress': feedbacks.filter(status='in_progress').count(),
                'resolved': feedbacks.filter(status='resolved').count(),
            },
            'feedback_types': {
                'bug': feedbacks.filter(feedback_type='bug').count(),
                'feature': feedbacks.filter(feedback_type='feature').count(),
                'improvement': feedbacks.filter(feedback_type='improvement').count(),
                'general': feedbacks.filter(feedback_type='general').count(),
            }
        })
    else:
        # User view with their own feedback
        feedbacks = Feedback.objects.filter(user=request.user).order_by('-date_submitted')
        
        context.update({
            'feedbacks': feedbacks,
            'feedback_stats': {
                'total': feedbacks.count(),
                'pending': feedbacks.filter(status='pending').count(),
                'in_progress': feedbacks.filter(status='in_progress').count(),
                'resolved': feedbacks.filter(status='resolved').count(),
            }
        })

    return render(request, 'feedback/feedback.html', context)

@login_required
@require_http_methods(["POST"])
def feedback_create(request):
    """
    Handle creation of new feedback.
    """
    form = FeedbackForm(request.POST)
    if form.is_valid():
        try:
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, 'Your feedback has been submitted successfully!')
        except Exception as e:
            messages.error(request, f'An error occurred while submitting feedback: {str(e)}')
    else:
        error_messages = []
        for field, errors in form.errors.items():
            for error in errors:
                error_messages.append(f"{field.capitalize()}: {error}")
        messages.error(request, 'Please correct the following errors: ' + ' '.join(error_messages))
    
    return redirect('feedback:feedback-list')

@login_required
def feedback_edit(request, pk):
    """
    Handle editing of existing feedback with improved error handling
    """
    feedback = get_object_or_404(Feedback, pk=pk)
    
    # Ensure user owns this feedback
    if feedback.user != request.user:
        messages.error(request, 'You do not have permission to edit this feedback.')
        return redirect('feedback:feedback-list')

    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feedback updated successfully!')
        else:
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field.capitalize()}: {error}")
            messages.error(request, 'Please correct the following errors: ' + ' '.join(error_messages))
    
    return redirect('feedback:feedback-list')

@login_required
@require_http_methods(["POST"])
def feedback_delete(request, pk):
    """
    Handle deletion of feedback.
    """
    feedback = get_object_or_404(Feedback, pk=pk)
    
    # Check if user owns this feedback
    if feedback.user != request.user:
        raise PermissionDenied
        
    try:
        feedback.delete()
        messages.success(request, 'Feedback deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting feedback: {str(e)}')
    
    return redirect('feedback:feedback-list')

@login_required
@user_passes_test(lambda u: u.is_staff)
@require_http_methods(["POST"])
def update_status(request, pk):
    """
    Handle status updates for feedback (staff only).
    """
    try:
        feedback = get_object_or_404(Feedback, pk=pk)
        data = json.loads(request.body)
        new_status = data.get('status')
        
        if new_status in dict(Feedback.STATUS_CHOICES):
            feedback.status = new_status
            feedback.save()
            return JsonResponse({
                'success': True,
                'message': f'Status updated to {feedback.get_status_display()}'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Invalid status value'
            }, status=400)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
def feedback_detail_api(request, pk):
    """
    API endpoint to get feedback details with improved response format
    """
    try:
        feedback = get_object_or_404(Feedback, pk=pk)
        
        # Check if user owns this feedback or is staff
        if feedback.user != request.user and not request.user.is_staff:
            return JsonResponse({
                'success': False,
                'error': 'Permission denied'
            }, status=403)
            
        return JsonResponse({
            'success': True,
            'data': {
                'id': feedback.pk,
                'type': feedback.feedback_type,  # Return the actual value, not display
                'subject': feedback.subject,
                'description': feedback.description,
                'status': feedback.status,
                'date_submitted': feedback.date_submitted.strftime('%B %d, %Y'),
                'user': feedback.user.username
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)