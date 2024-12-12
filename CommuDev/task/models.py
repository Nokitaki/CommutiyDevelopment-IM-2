# task/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High')
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled')
    ]

    task_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    reward_points = models.PositiveIntegerField(default=0, help_text="Reward points for completing this task/event")
    created_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tasks'
    )
    assigned_to = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='TaskAssignment',
        related_name='assigned_tasks'
    )
    is_event = models.BooleanField(default=False)
    location = models.CharField(max_length=200, blank=True, null=True)
    max_participants = models.PositiveIntegerField(default=0)  # 0 means unlimited

    def __str__(self):
        return f"{self.title} - Created by {self.created_by.firstname} {self.created_by.lastname}"

    class Meta:
        ordering = ['-created_date']

class TaskAssignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    assigned_date = models.DateTimeField(default=timezone.now)
    completed_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Task.STATUS_CHOICES, default='PENDING')

    class Meta:
        unique_together = ['task', 'user']

    def __str__(self):
        return f"{self.task.title} - Assigned to {self.user.firstname} {self.user.lastname}"

class TaskComment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f"Comment by {self.user.firstname} {self.user.lastname} on {self.task.title}"