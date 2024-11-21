from django.db import models

# Create your models here.
class Messaging(models.Model):
    username = models.CharField(max_length=255)
    message = models.TextField(max_length=2000)
    receiver = models.CharField(max_length=255)
