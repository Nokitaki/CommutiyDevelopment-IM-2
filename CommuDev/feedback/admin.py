#feedback/admin.py
from django.contrib import admin

from feedback.models import Feedback

# Register your models here.
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback_id', 'user_id', 'feedback_type', 'subject', 'date_submitted', 'date_resolved')
    search_fields = ('subject', 'feedback_type')
    list_filter = ('feedback_type', 'date_submitted')
    ordering = ('-date_submitted',)
    
admin.site.register(Feedback, FeedbackAdmin)