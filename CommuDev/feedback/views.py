
from django.urls import reverse_lazy
from django.views import generic
from .models import Feedback
from .forms import FeedbackForm


# Feedback Views
class FeedbackListView(generic.ListView):
    model = Feedback
    template_name = 'feedback/list.html'
    context_object_name = 'feedbacks'

class FeedbackCreateView(generic.CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback/create.html'
    success_url = reverse_lazy('feedback-list')  # Update if using namespace

class FeedbackUpdateView(generic.UpdateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback/edit.html'
    success_url = reverse_lazy('feedback-list')
    pk_url_kwarg = 'pk'

    def get_queryset(self):
        return Feedback.objects.all()

class FeedbackDeleteView(generic.DeleteView):
    model = Feedback
    template_name = 'feedback/confirm_delete.html'
    success_url = reverse_lazy('feedback-list')  # Update if using namespace