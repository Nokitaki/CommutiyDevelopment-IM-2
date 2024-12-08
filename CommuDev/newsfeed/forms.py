#newsfeed/forms.py
from django import forms
from .models import NewsFeed


class NewsFeedForm(forms.ModelForm):
    class Meta:
        model = NewsFeed
        fields = ['post_description']
        widgets = {
            'post_description': forms.Textarea(attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'rows': '3',
                'placeholder': "What's on your mind?"
            })
        }