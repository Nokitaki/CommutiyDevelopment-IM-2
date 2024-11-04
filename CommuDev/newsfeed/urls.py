from django.urls import path
from .views import home, create_post, like_post, update_post, delete_post

urlpatterns = [
    path('', home, name='home'),  # Home page showing posts
    path('create/', create_post, name='create_post'),  # Create a new post
    path('like/<int:post_id>/', like_post, name='like_post'),  # Like a specific post
    path('update/<int:id>/', update_post, name='update_post'),  # Update an existing post
    path('delete/<int:id>/', delete_post, name='delete_post'),  # Delete a post
]
