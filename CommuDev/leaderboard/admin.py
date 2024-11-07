from django.contrib import admin
from .models import Leaderboard


# Register your models here.
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('uid', 'username', 'rank', 'score')
    search_fields = ('username',)
    ordering = ('rank',)

admin.site.register(Leaderboard)