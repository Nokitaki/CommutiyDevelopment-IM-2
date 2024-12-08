from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'firstname', 'lastname', 'age', 
                 'state', 'employmentStatus', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username'
            }),
            'firstname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name'
            }),
            'lastname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter age'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter state'
            }),
            'employmentStatus': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter employment status'
            })
        }

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'age', 
                 'state', 'employmentStatus', 'profile_picture']
        widgets = {
            'firstname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name'
            }),
            'lastname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter age'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter state'
            }),
            'employmentStatus': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter employment status'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control-file'
            })
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields optional for editing
        for field in self.fields:
            self.fields[field].required = False