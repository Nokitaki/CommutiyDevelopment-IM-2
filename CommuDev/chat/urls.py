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
    path('message/edit/<int:message_id>/', views.edit_message, name='edit_message'),
    path('message/unsend/<int:message_id>/', views.unsend_message, name='unsend_message'),
    path('conversation/delete/<uuid:user_id>/', views.delete_conversation, name='delete_conversation'),
]