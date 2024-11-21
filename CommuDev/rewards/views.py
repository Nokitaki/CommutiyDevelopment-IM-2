# rewards/views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from .models import Reward
from .forms import RewardForm
from django.shortcuts import render, redirect, get_object_or_404

@login_required
def reward_list(request):
   rewards = Reward.objects.filter(user=request.user)
   return render(request, 'rewards/list.html', {'rewards': rewards})

@login_required
def reward_create(request):
   if request.method == 'POST':
       form = RewardForm(request.POST)
       if form.is_valid():
           reward = form.save(commit=False)
           reward.creator = request.user  # Set the creator to logged in user
           reward.user = request.user  # Set initial user (can be changed later)
           reward.save()
           return redirect('reward-list')
   else:
       form = RewardForm()
   return render(request, 'rewards/create.html', {'form': form})

@login_required
def reward_update(request, pk):
   reward = get_object_or_404(Reward, pk=pk, user=request.user)
   if request.method == 'POST':
       form = RewardForm(request.POST, instance=reward)
       if form.is_valid():
           form.save()
           return redirect('reward-list')
   else:
       form = RewardForm(instance=reward)
   return render(request, 'rewards/edit.html', {'form': form})

@login_required
def reward_delete(request, pk):
   reward = get_object_or_404(Reward, pk=pk, user=request.user)
   if request.method == 'POST':
       reward.delete()
       return redirect('reward-list')
   return render(request, 'rewards/delete.html', {'reward': reward})