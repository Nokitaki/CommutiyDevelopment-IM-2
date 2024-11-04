from django import forms
from .models import ResourceHub

class ResourceForm(forms.ModelForm):
    class Meta:
        model = ResourceHub
        fields = ['resource_title', 'resource_description', 'resource_category']
