# resourcehub/models.py
from django.db import models
from users.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class ResourceHub(models.Model):
    resource_id = models.AutoField(primary_key=True)
    resource_title = models.CharField(max_length=200)
    resource_description = models.TextField(help_text="HTML content allowed")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resources')
    upload_date = models.DateTimeField(auto_now_add=True)
    download_count = models.IntegerField(default=0)
    image = models.ImageField(upload_to='resources/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='resources')

    def __str__(self):
        return self.resource_title