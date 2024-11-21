# newsfeed/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_post, name='create_post'),
    path('like/<int:feed_id>/', views.like_post, name='like_post'),
    path('update/<int:feed_id>/', views.update_post, name='update_post'),
    path('delete/<int:feed_id>/', views.delete_post, name='delete_post'),
]