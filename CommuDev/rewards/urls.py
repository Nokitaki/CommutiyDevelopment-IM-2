#resourcehub/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.reward_list, name='reward-list'),
    path('create/', views.reward_create, name='reward-create'),
    path('edit/<int:pk>/', views.reward_update, name='reward-edit'),
    path('delete/<int:pk>/', views.reward_delete, name='reward-delete'),
]