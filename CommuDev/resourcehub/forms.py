from django import forms
from .models import ResourceHub, Category
from django.utils.html import strip_tags
import bleach

class ResourceForm(forms.ModelForm):
    class Meta:
        model = ResourceHub
        fields = ['resource_title', 'resource_description', 'image', 'category']
        widgets = {
            'resource_title': forms.TextInput(attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Enter resource title'
            }),
            'resource_description': forms.Textarea(attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'rows': '3',
                'placeholder': 'Enter resource description'
            }),
            'category': forms.Select(attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'image': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'
            })
        }
    