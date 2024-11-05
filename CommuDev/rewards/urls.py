from django.urls import path

import rewards.views as views


urlpatterns = [
    path('', views.RewardListView.as_view(), name='reward-list'),
    path('create/', views.RewardCreateView.as_view(), name='reward-create'),
    path('edit/<int:pk>/', views.RewardUpdateView.as_view(), name='reward-edit'),
    path('delete/<int:pk>/', views.RewardDeleteView.as_view(), name='reward-delete'),
]