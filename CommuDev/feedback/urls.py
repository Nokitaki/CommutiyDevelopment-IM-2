# urls.py
from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('', views.feedback_list, name='feedback-list'),
    path('create/', views.feedback_create, name='feedback-create'),
    path('edit/<int:pk>/', views.feedback_edit, name='feedback-edit'),
    path('delete/<int:pk>/', views.feedback_delete, name='feedback-delete'),
    path('update-status/<int:pk>/', views.update_status, name='update-status'),
    path('api/feedback/<int:pk>/', views.feedback_detail_api, name='feedback-detail-api'),
]