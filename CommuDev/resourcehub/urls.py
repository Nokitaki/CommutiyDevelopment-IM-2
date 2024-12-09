# resourcehub/urls.py
from django.urls import path
from .views import create_resource, like_resource, update_resource, delete_resource, resource_list
from . import views
urlpatterns = [
    path('', resource_list, name='resource_home'),  # Main resource list view
    path('create/', create_resource, name='create_resource'),  # Create a new resource
    path('like/<int:resource_id>/', like_resource, name='like_resource'),  # Like a resource
    path('update/<int:resource_id>/', update_resource, name='update_resource'),  # Update a resource
    path('delete/<int:resource_id>/', delete_resource, name='delete_resource'),  # Delete a resource
    path('get/<int:resource_id>/', views.get_resource_details, name='get_resource_details'),
    path('download/<int:resource_id>/', views.download_resource, name='download_resource'),
    path('upload/', views.upload_image, name='upload_image'),
]