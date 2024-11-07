# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('user/create/', views.user_create, name='user_create'),
    path('user/<uuid:pk>/edit/', views.user_update, name='user_update'),
    path('user/<uuid:pk>/delete/', views.user_delete, name='user_delete'),
    path('', views.index, name='user_index'), 
]