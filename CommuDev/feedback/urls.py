from django.urls import path
import feedback.views as views

urlpatterns = [
  
    # Feedback URLs
    path('list/', views.FeedbackListView.as_view(), name='feedback-list'),
    path('create/', views.FeedbackCreateView.as_view(), name='feedback-create'),
    path('edit/<int:pk>/', views.FeedbackUpdateView.as_view(), name='feedback-edit'),
    path('delete/<int:pk>/', views.FeedbackDeleteView.as_view(), name='feedback-delete'),
]