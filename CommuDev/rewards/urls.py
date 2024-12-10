# rewards/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # User URLs
    path('', views.reward_list, name='reward-list'),
    path('redeem-code/', views.redeem_code, name='redeem-code'),
    path('redeem/<int:reward_id>/', views.redeem_reward, name='redeem-reward'),
    
    # Admin URLs (staff only)
    path('create/', views.reward_create, name='reward-create'),
    path('edit/<int:pk>/', views.reward_update, name='reward-edit'),
    path('delete/<int:pk>/', views.reward_delete, name='reward-delete'),
    path('generate-codes/', views.generate_codes, name='generate-codes'),
    
    # API endpoints for AJAX calls
    path('api/check-points/', views.check_points, name='check-points'),
    path('api/reward-stats/', views.reward_stats, name='reward-stats'),
    
    path('reward/<int:pk>/', views.reward_detail, name='reward-detail'),  # For viewing individual rewards
    path('rewards/user/', views.user_rewards, name='user-rewards'),

]