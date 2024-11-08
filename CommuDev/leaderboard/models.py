from django.db import models
import uuid

# Create your models here.
class Leaderboard(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100)
    score = models.IntegerField()

    def __str__(self):
        return f'{self.username} - Score: {self.score}'


    @staticmethod
    def get_rank(user_id):
        leaderboard = Leaderboard.objects.all().order_by('-score')
        for index, entry in enumerate(leaderboard):
            if entry.uid == user_id:
                return index + 1
        return None