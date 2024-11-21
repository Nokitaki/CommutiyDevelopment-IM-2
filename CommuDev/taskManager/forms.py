# taskManager/forms.py
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_description', 'status', 'priority', 'due_date', 'task_type', 'reward']
        widgets = {
            'task_description': forms.Textarea(attrs={
                'class': 'w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'rows': '4'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'priority': forms.Select(attrs={
                'class': 'w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'task_type': forms.Select(attrs={
                'class': 'w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'reward': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            })
        }