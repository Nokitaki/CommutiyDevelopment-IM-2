# rewards/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Reward, UserPoints, RedemptionCode
from .forms import RewardForm

def reward_list(request):
    # Start with all rewards
    rewards = Reward.objects.filter(is_active=True)
    user_points, created = UserPoints.objects.get_or_create(user=request.user)

    # Apply filters from GET parameters
    min_points = request.GET.get('min_points')
    max_points = request.GET.get('max_points')
    availability = request.GET.get('availability')
    sort_by = request.GET.get('sort')

    # Points range filter
    if min_points:
        rewards = rewards.filter(points_required__gte=min_points)
    if max_points:
        rewards = rewards.filter(points_required__lte=max_points)

    # Availability filter
    if availability == 'available':
        rewards = rewards.filter(quantity__gt=0)
    elif availability == 'affordable':
        rewards = rewards.filter(
            Q(points_required__lte=user_points.points) & Q(quantity__gt=0)
        )

    # Sorting
    if sort_by == 'points-low':
        rewards = rewards.order_by('points_required')
    elif sort_by == 'points-high':
        rewards = rewards.order_by('-points_required')
    elif sort_by == 'quantity':
        rewards = rewards.order_by('-quantity')
    else:
        rewards = rewards.order_by('-created_at')  # Default to newest

    context = {
        'rewards': rewards,
        'user_points': user_points,
        'top_redeemers': UserPoints.objects.order_by('-points')[:5],
        'form': RewardForm() if request.user.is_staff else None,
        'daily_redemptions': Reward.objects.filter(user__isnull=False).count()
    }
    return render(request, 'rewards/list.html', context)

def reward_create(request):
    if request.method == 'POST':
        form = RewardForm(request.POST, request.FILES)
        if form.is_valid():
            reward = form.save(commit=False)
            reward.creator = request.user
            reward.save()
            return redirect('reward-list')
    return redirect('reward-list')

def reward_update(request, pk):
    reward = get_object_or_404(Reward, pk=pk)
    if request.method == 'POST':
        form = RewardForm(request.POST, request.FILES, instance=reward)
        if form.is_valid():
            form.save()
            return redirect('reward-list')
    return redirect('reward-list')

def reward_delete(request, pk):
    reward = get_object_or_404(Reward, pk=pk)
    if request.method == 'POST':
        reward.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def generate_codes(request):
    if request.method == 'POST':
        points = int(request.POST.get('points', 0))
        quantity = min(int(request.POST.get('quantity', 1)), 100)
        
        codes = []
        for _ in range(quantity):
            code = RedemptionCode.objects.create(
                code=RedemptionCode.generate_code(),
                points=points
            )
            codes.append(code.code)
            
        return JsonResponse({'success': True, 'codes': codes})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def redeem_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            redemption_code = RedemptionCode.objects.get(code=code, is_redeemed=False)
            user_points, created = UserPoints.objects.get_or_create(user=request.user)
            
            user_points.points += redemption_code.points
            user_points.save()
            
            redemption_code.is_redeemed = True
            redemption_code.redeemed_by = request.user
            redemption_code.save()
            
            return redirect('reward-list')
        except RedemptionCode.DoesNotExist:
            return redirect('reward-list')
    return redirect('reward-list')

def redeem_reward(request, reward_id):
    reward = get_object_or_404(Reward, reward_id=reward_id)
    user_points = get_object_or_404(UserPoints, user=request.user)
    
    if user_points.points >= reward.points_required and reward.quantity > 0:
        user_points.points -= reward.points_required
        user_points.save()
        
        reward.quantity -= 1
        reward.user = request.user
        reward.save()
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Unable to redeem reward'})

def check_points(request):
    user_points = UserPoints.objects.get(user=request.user)
    return JsonResponse({'points': user_points.points})

def reward_stats(request):
    total_rewards = Reward.objects.count()
    available_rewards = Reward.objects.filter(quantity__gt=0).count()
    return JsonResponse({
        'total_rewards': total_rewards,
        'available_rewards': available_rewards
    })
    
def reward_detail(request, pk):
    """View for displaying individual reward details"""
    reward = get_object_or_404(Reward, pk=pk)
    context = {
        'reward': reward,
        'user_points': UserPoints.objects.get_or_create(user=request.user)[0]
    }
    return render(request, 'rewards/detail.html', context)

def user_rewards(request):
    """View for displaying user's claimed rewards"""
    user_rewards = Reward.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'rewards': user_rewards,
        'user_points': UserPoints.objects.get_or_create(user=request.user)[0]
    }
    return render(request, 'rewards/user_rewards.html', context)
