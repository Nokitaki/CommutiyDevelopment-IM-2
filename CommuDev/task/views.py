# task/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import Task, TaskAssignment, TaskComment
from .forms import TaskForm, TaskCommentForm

def is_staff_check(user):
    return user.is_staff

@login_required
def task_list(request):
    filter_type = request.GET.get('filter', 'all')
    
    if filter_type == 'assigned':
        tasks = Task.objects.filter(assigned_to=request.user)
    elif filter_type == 'available':
        tasks = Task.objects.filter(is_event=True).exclude(assigned_to=request.user)
    else:  # 'all'
        tasks = Task.objects.all()
    
    context = {
        'tasks': tasks,
        'pending_count': TaskAssignment.objects.filter(
            user=request.user, 
            status='PENDING'
        ).count(),
        'in_progress_count': TaskAssignment.objects.filter(
            user=request.user, 
            status='IN_PROGRESS'
        ).count(),
        'completed_count': TaskAssignment.objects.filter(
            user=request.user, 
            status='COMPLETED'
        ).count(),
        'upcoming_events': Task.objects.filter(
            is_event=True, 
            due_date__gte=timezone.now()
        ).order_by('due_date')[:5]
    }
    return render(request, 'task/task_list.html', context)

@login_required
@user_passes_test(is_staff_check)
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task:task_list')
    else:
        form = TaskForm()
    
    return render(request, 'task/task_form.html', {'form': form})

@login_required
def join_task(request, task_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
        
    task = get_object_or_404(Task, task_id=task_id)
    
    try:
        # Check if user is already a participant
        if request.user in task.assigned_to.all():
            return JsonResponse({
                'status': 'error',
                'message': 'You are already a participant'
            })
            
        # Check maximum participants
        if task.max_participants > 0 and task.assigned_to.count() >= task.max_participants:
            return JsonResponse({
                'status': 'error',
                'message': 'This event has reached its maximum number of participants'
            })
            
        # Create the assignment
        TaskAssignment.objects.create(
            task=task,
            user=request.user,
            status='PENDING'
        )
        
        return JsonResponse({
            'status': 'success',
            'message': f'Successfully joined {task.title}',
            'participants_count': task.assigned_to.count()
        })
            
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

@login_required
def leave_task(request, task_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
        
    task = get_object_or_404(Task, task_id=task_id)
    
    try:
        assignment = TaskAssignment.objects.get(task=task, user=request.user)
        assignment.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Successfully left {task.title}',
            'participants_count': task.assigned_to.count()
        })
            
    except TaskAssignment.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'You are not a participant in this event'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, task_id=task_id)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'task_id': task.task_id,
            'title': task.title,
            'description': task.description,
            'created_date': task.created_date.isoformat(),
            'due_date': task.due_date.isoformat(),
            'priority': task.priority,
            'status': task.status,
            'is_event': task.is_event,
            'location': task.location,
            'max_participants': task.max_participants,
            'participants_count': task.assigned_to.count(),
            'is_participant': request.user in task.assigned_to.all(),
            'created_by': {
                'firstname': task.created_by.firstname,
                'lastname': task.created_by.lastname,
            }
        })
    
    # For non-AJAX requests, redirect to task list
    return redirect('task:task_list')

@login_required
def update_task_status(request, task_id):
    if not request.user.is_staff:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'})
        
    task = get_object_or_404(Task, task_id=task_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Task.STATUS_CHOICES):
            task.status = new_status
            task.save()
            
            # Update all assignments status
            if new_status in ['COMPLETED', 'CANCELLED']:
                task.taskassignment_set.all().update(
                    status=new_status,
                    completed_date=timezone.now() if new_status == 'COMPLETED' else None
                )
                
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid status'})

@login_required
def update_assignment_status(request, task_id):
    task = get_object_or_404(Task, task_id=task_id)
    assignment = get_object_or_404(TaskAssignment, task=task, user=request.user)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Task.STATUS_CHOICES):
            assignment.status = new_status
            if new_status == 'COMPLETED':
                assignment.completed_date = timezone.now()
            assignment.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

@login_required
@user_passes_test(is_staff_check)
def edit_task(request, task_id):
    task = get_object_or_404(Task, task_id=task_id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'errors': form.errors})
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    })
    
@login_required
@user_passes_test(is_staff_check)
def delete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, task_id=task_id)
        task.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    })