# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['firstname', 'middleinit', 'lastname', 'username', 'age', 
                 'state', 'employmentStatus', 'password1', 'password2']