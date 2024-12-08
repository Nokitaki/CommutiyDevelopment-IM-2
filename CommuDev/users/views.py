from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserProfileEditForm
from .models import User

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        except User.DoesNotExist:
            pass
        messages.error(request, 'Invalid username or password.')
    return render(request, 'users/login.html')

@login_required
def profile(request):
    """View function for the user profile page."""
    return render(request, 'users/profile.html', {
        'user': request.user,
        'title': 'Profile',
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileEditForm(instance=request.user)
    
    context = {
        'form': form,
        'title': 'Edit Profile', 
        'submit_text': 'Save Changes'  
    }
    return render(request, 'users/user_form.html', context)