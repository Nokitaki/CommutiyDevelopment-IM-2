from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import ValidationError
from .models import User
from .forms import UserForm

def user_list(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        users = User.objects.filter(
            Q(firstname__icontains=search_query) |
            Q(lastname__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(state__icontains=search_query)
        )
    else:
        users = User.objects.all()
    
    context = {
        'users': users,
        'search_query': search_query
    }
    return render(request, 'users/user_list.html', context)

def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        try:
            if form.is_valid():
                user = form.save(commit=False)
                user.clean()  # Run model validation
                user.save()
                messages.success(request, 'User created successfully!')
                return redirect('user_list')
            else:
                messages.error(request, 'Please correct the errors below.')
        except ValidationError as e:
            messages.error(request, str(e))
    else:
        form = UserForm()
    
    return render(request, 'users/user_form.html', {
        'form': form,
        'title': 'Add User',
        'submit_text': 'Create User'
    })

def user_update(request, pk):
    user = get_object_or_404(User, userId=pk)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        try:
            if form.is_valid():
                user = form.save(commit=False)
                user.clean()  # Run model validation
                user.save()
                messages.success(request, 'User updated successfully!')
                return redirect('user_list')
            else:
                messages.error(request, 'Please correct the errors below.')
        except ValidationError as e:
            messages.error(request, str(e))
    else:
        form = UserForm(instance=user)
    
    return render(request, 'users/user_form.html', {
        'form': form,
        'title': 'Edit User',
        'submit_text': 'Update User',
        'user': user
    })

def user_delete(request, pk):
    user = get_object_or_404(User, userId=pk)
    
    if request.method == 'POST':
        try:
            user.delete()
            messages.success(request, 'User deleted successfully!')
            return redirect('user_list')
        except Exception as e:
            messages.error(request, f'Error deleting user: {str(e)}')
            return redirect('user_list')
    
    return render(request, 'users/user_confirm_delete.html', {
        'user': user
    })

def user_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/user_profile.html', {'user': user})

def index(request):
    return render(request, 'users/index.html')