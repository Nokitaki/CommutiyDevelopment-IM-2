from django.db import models
from django.contrib.auth.models import User  

class Task(models.Model):
    task_description = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed')
    ])
    priority = models.CharField(max_length=20, choices=[
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High')
    ])
    due_date = models.DateField()
    task_type = models.CharField(max_length=50, choices=[
        ('GENERAL', 'General'),
        ('COMMUNITY_SERVICE', 'Community Service'),
        ('EDUCATION', 'Education'),
        ('ENVIRONMENT', 'Environment'),
        ('HEALTHCARE', 'Healthcare')
    ])
    reward = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    completed_date = models.DateField(null=True, blank=True)  

    def __str__(self):
        return self.task_description
