#taskManager/models.py
from django.db import models
from django.conf import settings


class Task(models.Model):
    creator = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='tasks'
)
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
    completed_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.task_description

    def get_status_color(self):
        return {
            'PENDING': 'yellow',
            'IN_PROGRESS': 'blue',
            'COMPLETED': 'green'
        }.get(self.status, 'gray')

    def get_priority_color(self):
        return {
            'LOW': 'green',
            'MEDIUM': 'yellow',
            'HIGH': 'red'
        }.get(self.priority, 'gray')