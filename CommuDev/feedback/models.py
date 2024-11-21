#feedback/models.py
from django.conf import settings
from django.db import models
from django.urls import reverse


class Feedback(models.Model):
    FEEDBACK_TYPES = [
        ('bug', 'Bug Report'),
        ('feature', 'Feature Request'),
        ('general', 'General Feedback'),
    ]

    feedback_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedbacks')
    feedback_type = models.CharField(max_length=100, choices=FEEDBACK_TYPES)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)
    date_resolved = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['-date_submitted']