from django.contrib import admin

from rewards.models import Reward

# Register your models here.

class RewardAdmin(admin.ModelAdmin):
    list_display = ('reward_id', 'name', 'value', 'quantity', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)

admin.site.register(Reward, RewardAdmin)