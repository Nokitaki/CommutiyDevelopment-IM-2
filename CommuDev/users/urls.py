from django.urls import path
from django.contrib.auth.views import LogoutView  # Import Django's built-in LogoutView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),  # Use Django's built-in LogoutView
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]