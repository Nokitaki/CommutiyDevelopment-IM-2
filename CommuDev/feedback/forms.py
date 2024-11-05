from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback_type', 'subject', 'description']
        widgets = {
            'feedback_type': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }