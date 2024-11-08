# users/forms.py

from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['firstname', 'middleinit', 'lastname', 'username', 'age', 'state', 'employmentStatus']