# task/urls.py
from django.urls import path
from . import views

app_name = 'task'

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.create_task, name='create_task'),
    path('<int:task_id>/', views.task_detail, name='task_detail'),
    path('<int:task_id>/join/', views.join_task, name='join_task'),
    path('<int:task_id>/leave/', views.leave_task, name='leave_task'),
    path('<int:task_id>/update-status/', views.update_task_status, name='update_task_status'),
    path('<int:task_id>/update-assignment/', views.update_assignment_status, name='update_assignment_status'),
    path('<int:task_id>/detail/', views.task_detail, name='task_detail'),
    path('<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('<int:task_id>/delete/', views.delete_task, name='delete_task'),
]