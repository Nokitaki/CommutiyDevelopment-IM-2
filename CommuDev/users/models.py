# users/models.py

from django.db import models
import uuid

class User(models.Model):
    userId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname = models.CharField(max_length=100)
    middleinit = models.CharField(max_length=1, blank=True, null=True)
    lastname = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    age = models.IntegerField()
    state = models.CharField(max_length=100)
    employmentStatus = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"