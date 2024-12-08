# calendar_events/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_event, name='create_event'),
    path('get/', views.get_events, name='get_events'),
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
]