from django import forms

from rewards.models import Reward


class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = ['value', 'quantity', 'name']  # Adjust fields according to your model