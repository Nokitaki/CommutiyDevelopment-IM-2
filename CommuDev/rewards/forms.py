# rewards/forms.py
from django import forms
from .models import Reward, RedemptionCode

class RewardForm(forms.ModelForm):
    class Meta:
        error_messages = {
            'points_required': {'min_value': 'Points required must be greater than 0'},
            'quantity': {'min_value': 'Quantity must be greater than 0'}
        }
        model = Reward
        fields = ['name', 'description', 'points_required', 'quantity', 'value', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded-lg mb-2',
                'placeholder': 'Enter reward name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded-lg mb-2',
                'placeholder': 'Enter description',
                'rows': 3
            }),
            'points_required': forms.NumberInput(attrs={
                'class': 'w-full p-2 border rounded-lg mb-2',
                'placeholder': 'Required points'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'w-full p-2 border rounded-lg mb-2',
                'placeholder': 'Available quantity'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full p-2 border rounded-lg mb-2'
            }),
            'value': forms.NumberInput(attrs={
                'class': 'w-full p-2 border rounded-lg mb-2',
                'placeholder': 'Enter value in Peso',
                'min': '0.01',
                'step': '0.01'
            }),
        }
        labels = {
            'value': 'Value in Peso (₱)'
        }

class CodeGenerationForm(forms.Form):
    points = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'w-full p-2 border rounded-lg mb-2',
            'placeholder': 'Points per code'
        })
    )
    quantity = forms.IntegerField(
        min_value=1,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'w-full p-2 border rounded-lg mb-2',
            'placeholder': 'Number of codes to generate'
        })
    )