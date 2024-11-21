# message/urls.py
from django.urls import path
from . import views

urlpatterns = [
   path('', views.user_message_list, name='user_message_list'),
   path('create/', views.user_message_create, name='user_message_create'),
   path('<int:user_message_id>/message/create/', views.message_create, name='message_create'),
]