#rewards/model.py
from django.db import models
from django.urls import reverse
from django.conf import settings

class Reward(models.Model):
    reward_id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_rewards')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='claimed_rewards')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('reward-list')