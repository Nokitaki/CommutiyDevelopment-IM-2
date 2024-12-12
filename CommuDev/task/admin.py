# task/admin.py
from django.contrib import admin
from .models import Task, TaskAssignment, TaskComment

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'due_date', 'status', 'priority', 'is_event')
    list_filter = ('status', 'priority', 'is_event', 'created_date')
    search_fields = ('title', 'description', 'created_by__firstname', 'created_by__lastname')
    date_hierarchy = 'due_date'
    ordering = ('-created_date',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'created_by', 'due_date')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority')
        }),
        ('Event Details', {
            'fields': ('is_event', 'location', 'max_participants'),
            'classes': ('collapse',)
        })
    )

@admin.register(TaskAssignment)
class TaskAssignmentAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'assigned_date', 'completed_date', 'status')
    list_filter = ('status', 'assigned_date', 'completed_date')
    search_fields = ('task__title', 'user__firstname', 'user__lastname')
    date_hierarchy = 'assigned_date'
    ordering = ('-assigned_date',)

@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'created_date', 'content_preview')
    list_filter = ('created_date',)
    search_fields = ('task__title', 'user__firstname', 'user__lastname', 'content')
    date_hierarchy = 'created_date'
    ordering = ('-created_date',)

    def content_preview(self, obj):
        """Return first 50 characters of the comment content"""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Comment'