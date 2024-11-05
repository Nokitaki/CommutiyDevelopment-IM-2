from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .models import Reward
from .forms import RewardForm

# Reward Views
class RewardListView(generic.ListView):
    model = Reward
    template_name = 'rewards/list.html'
    context_object_name = 'rewards'

class RewardCreateView(generic.CreateView):
    model = Reward
    template_name = 'rewards/create.html'
    form_class = RewardForm
    success_url = reverse_lazy('reward-list')  # Update if using namespace
    
class RewardUpdateView(generic.UpdateView):
    model = Reward
    template_name = 'rewards/edit.html'
    form_class = RewardForm
    success_url = reverse_lazy('reward-list')  # Update if using namespace

class RewardDeleteView(generic.DeleteView):
    model = Reward
    template_name = 'rewards/delete.html'
    success_url = reverse_lazy('reward-list')  # Update if using namespace