from django.contrib import admin
from .models import Issue

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('tracking_id', 'title', 'department', 'status', 'created_at')
    list_filter = ('status', 'department', 'created_at')
    search_fields = ('tracking_id', 'title', 'description', 'location')
    list_editable = ('status',)