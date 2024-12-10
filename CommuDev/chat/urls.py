# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_home, name='chat_home'),
    path('contacts/', views.get_contacts, name='get_contacts'),
    path('messages/<uuid:user_id>/', views.get_messages, name='get_messages'),
    path('send/', views.send_message, name='send_message'),
    path('unread-count/', views.get_unread_count, name='get_unread_count'),
    path('mark-read/<uuid:user_id>/', views.mark_messages_read, name='mark_messages_read'),
]