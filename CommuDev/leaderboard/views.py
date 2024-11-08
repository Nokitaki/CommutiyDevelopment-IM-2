from django.shortcuts import render
from .models import Leaderboard

# Create your views here.
def leaderboard_view(request):
    # Get all users ordered by score (high to low)
    leaderboard = Leaderboard.objects.all().order_by('-score')
    
    # Assign ranks dynamically in the view
    for index, entry in enumerate(leaderboard):
        entry.rank = index + 1

    return render(request, 'leaderboard.html', {'leaderboard': leaderboard})