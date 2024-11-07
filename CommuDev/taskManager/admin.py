# tasks/admin.py
from django.contrib import admin
from .models import Task  

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_description', 'status', 'due_date')  
