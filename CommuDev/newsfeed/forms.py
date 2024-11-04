from django import forms
from .models import NewsFeed

class NewsFeedForm(forms.ModelForm):
    class Meta:
        model = NewsFeed
        fields = ['post_description']  
