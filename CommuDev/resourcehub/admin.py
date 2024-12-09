from django.contrib import admin
from .models import Category, ResourceHub

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(ResourceHub)
class ResourceHubAdmin(admin.ModelAdmin):
    list_display = ('resource_title', 'created_by', 'category', 'upload_date')
    list_filter = ('category', 'upload_date')
    search_fields = ('resource_title', 'resource_description')