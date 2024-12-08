# newsfeed/models.py
from django.db import models
from django.utils import timezone
from users.models import User

class NewsFeed(models.Model):
    feed_id = models.AutoField(primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_posts')
    post_description = models.TextField(default="")
    post_date = models.DateTimeField(default=timezone.now)
    post_type = models.CharField(max_length=20, default='Active')
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    @property
    def like_count(self):
        return self.likes.count()

    def __str__(self):
        return f"Feed {self.feed_id} by {self.created_by}"