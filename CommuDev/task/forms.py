# task/forms.py
from django import forms
from .models import Task, TaskComment
from django.utils import timezone

class TaskForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500'
        })
    )
    reward_points = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500',
            'placeholder': 'Enter reward points'
        })
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'is_event', 
                 'location', 'max_participants', 'reward_points'] 
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Enter task title'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Enter task description'
            }),
            'priority': forms.Select(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Enter event location'
            }),
            'max_participants': forms.NumberInput(attrs={
                'class': 'w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500',
                'min': '0'
            })
        }

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < timezone.now():
            raise forms.ValidationError("Due date cannot be in the past")
        return due_date

class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Add your comment...'
            })
        }