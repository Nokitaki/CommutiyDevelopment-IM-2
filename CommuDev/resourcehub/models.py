from django.db import models

class ResourceHub(models.Model):
    resource_id = models.AutoField(primary_key=True)
    resource_title = models.CharField(max_length=255)
    resource_description = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    resource_category = models.CharField(max_length=100)
    heart_count = models.IntegerField(default=0)
    created_by = models.CharField(max_length=255, default="Anonymous")  # Temporary string field for creator's name

    def __str__(self):
        return self.resource_title
