from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    userId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname = models.CharField(max_length=100)
    middleinit = models.CharField(max_length=1, blank=True, null=True)
    lastname = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    state = models.CharField(max_length=100)
    employmentStatus = models.CharField(max_length=100)
    points = models.IntegerField(default=0)
    profile_picture = models.ImageField(upload_to='profile_pics', default='default.jpg')

    # Keep username for login purposes
    USERNAME_FIELD = 'username'  # This ensures username is used for login
    REQUIRED_FIELDS = ['firstname', 'lastname']  # Required fields for createsuperuser

    def __str__(self):
        return f"{self.firstname} {self.lastname}"