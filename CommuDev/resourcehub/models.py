# resourcehub/models.py
from django.db import models
from users.models import User

class ResourceHub(models.Model):
    resource_id = models.AutoField(primary_key=True)
    resource_title = models.CharField(max_length=200)
    resource_description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resources')
    upload_date = models.DateTimeField(auto_now_add=True)
    heart_count = models.IntegerField(default=0)

    def __str__(self):
        return self.resource_title