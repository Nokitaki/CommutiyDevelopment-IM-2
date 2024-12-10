# rewards/models.py
from django.db import models
from django.conf import settings
from django.urls import reverse
import random
import string

class UserPoints(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username}'s points: {self.points}"

class RedemptionCode(models.Model):
    code = models.CharField(max_length=12, unique=True)
    points = models.PositiveIntegerField()
    is_redeemed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    redeemed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    @staticmethod
    def generate_code():
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
            if not RedemptionCode.objects.filter(code=code).exists():
                return code
    
    def __str__(self):
        return f"Code: {self.code} - Points: {self.points}"

class Reward(models.Model):
    reward_id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_rewards')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='claimed_rewards', null=True, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    points_required = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='rewards/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('reward-list')
    
    def is_available(self):
        return self.quantity > 0 and self.is_active
    
    def points_per_peso(self):
        """Calculate points per peso ratio"""
        if self.value and self.value > 0:
            return round(float(self.points_required) / float(self.value), 2)
        return 0