#resourcehub/forms.py
from django import forms
from .models import ResourceHub

class ResourceForm(forms.ModelForm):
   class Meta:
       model = ResourceHub
       fields = ['resource_title', 'resource_description']  # Removed resource_category since it's not in the model
       widgets = {
           'resource_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter resource title'}),
           'resource_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter resource description'})
       }