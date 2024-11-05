from django.db import models
from django.urls import reverse
from django.conf import settings
# Create your models here.

class Reward(models.Model):
    reward_id = models.AutoField(primary_key=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rewards',
        null=True,  # Allow null for existing records
        blank=True  # Make it optional in forms
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('reward-list')