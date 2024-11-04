from django.urls import path
from .views import create_resource, like_resource, update_resource, delete_resource, resource_list

urlpatterns = [
    path('create/', create_resource, name='create_resource'),  # Path for creating a resource
    path('resources/like/<int:resource_id>/', like_resource, name='like_resource'),  # Path for liking a resource
    path('update/<int:resource_id>/', update_resource, name='update_resource'),  # Path for updating a resource
    path('resources/delete/<int:resource_id>/', delete_resource, name='delete_resource'),  # Path for deleting a resource
    path('', resource_list, name='resource_home'),  # Path for listing all resources
]
