from django.urls import path
from .views import send_message, edit_message, delete_message, MessageListView

urlpatterns = [
    path('send/', send_message, name='send_message'),
    path('<int:pk>/edit/', edit_message, name='edit_message'),
    path('<int:pk>/delete/', delete_message, name='delete_message'),
    path('', MessageListView.as_view(), name='message_list'),
]
