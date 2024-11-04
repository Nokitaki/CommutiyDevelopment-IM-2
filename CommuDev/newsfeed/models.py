from django.db import models
from django.utils import timezone

class NewsFeed(models.Model):
    created_by = models.CharField(max_length=255, default="Anonymous")  # Temporary string field for creator's name
    post_description = models.TextField(default="create a post")  # Input field for the post description
    post_date = models.DateTimeField(default=timezone.now)  # Automatically set the current date and time
    post_type = models.CharField(max_length=20, default='Active')  # Default post type set to 'Active'
    like_count = models.IntegerField(default=0)  # Like count, initially 0