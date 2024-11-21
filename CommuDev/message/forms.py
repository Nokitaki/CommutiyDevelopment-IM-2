# message/forms.py
from django import forms
from .models import UserMessage, Message

class UserMessageForm(forms.ModelForm):
   class Meta:
       model = UserMessage
       fields = ['subject', 'users']
       widgets = {
           'subject': forms.TextInput(attrs={'class': 'form-control'}),
           'users': forms.SelectMultiple(attrs={'class': 'form-control'})
       }

class MessageForm(forms.ModelForm):
   class Meta:
       model = Message  
       fields = ['content']
       widgets = {
           'content': forms.Textarea(attrs={'class': 'form-control'})
       }
