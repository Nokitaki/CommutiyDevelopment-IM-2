#feedback/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.feedback_list, name='feedback-list'),
    path('create/', views.feedback_create, name='feedback-create'),
    path('edit/<int:pk>/', views.feedback_update, name='feedback-edit'),
    path('delete/<int:pk>/', views.feedback_delete, name='feedback-delete'),
]