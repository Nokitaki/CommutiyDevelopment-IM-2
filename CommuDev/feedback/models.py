# models.py
from django.conf import settings
from django.db import models
from django.utils import timezone

class Feedback(models.Model):
    FEEDBACK_TYPES = [
        ('bug', 'Bug Report'),
        ('feature', 'Feature Request'),
        ('improvement', 'Improvement Suggestion'),
        ('general', 'General Feedback'),
        ('other', 'Other')
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed')
    ]
    
    feedback_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedbacks')
    feedback_type = models.CharField(max_length=100, choices=FEEDBACK_TYPES)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    date_submitted = models.DateTimeField(auto_now_add=True)
    date_resolved = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True, null=True)
    priority = models.CharField(
        max_length=20,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='medium'
    )
    
    class Meta:
        ordering = ['-date_submitted']
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'
        
    def __str__(self):
        return f"{self.subject} - {self.user.username}"
    
    def resolve(self, notes=None):
        self.status = 'resolved'
        self.date_resolved = timezone.now()
        if notes:
            self.resolution_notes = notes
        self.save()