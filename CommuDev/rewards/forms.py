# rewards/forms.py
from django import forms
from .models import Reward

class RewardForm(forms.ModelForm):
   class Meta:
       model = Reward
       exclude = ['user','creator']
       widgets = {
           'name': forms.TextInput(attrs={
               'class': 'form-control',
               'placeholder': 'Enter reward name'
           }),
           'value': forms.NumberInput(attrs={
               'class': 'form-control',
               'placeholder': 'Enter reward value' 
           }),
           'quantity': forms.NumberInput(attrs={
               'class': 'form-control',
               'placeholder': 'Enter quantity'
           })
       }