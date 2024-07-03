# main/admin.py
from django.contrib import admin
from .models import Issue

class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'issue', 'ward', 'image', 'status')
    list_filter = ('status', 'ward')
    search_fields = ('issue', 'ward')
    actions = ['mark_as_in_progress', 'mark_as_resolved', 'mark_as_open']

    def mark_as_in_progress(self, request, queryset):
        """Mark selected issues as 'In Progress'."""
        queryset.update(status='in_progress')
    mark_as_in_progress.short_description = "Mark selected issues as In Progress"

    def mark_as_resolved(self, request, queryset):
        """Mark selected issues as 'Resolved'."""
        queryset.update(status='resolved')
    mark_as_resolved.short_description = "Mark selected issues as Resolved"

    def mark_as_open(self, request, queryset):
        """Mark selected issues as 'Open'."""
        queryset.update(status='open')
    mark_as_open.short_description = "Mark selected issues as Open"

admin.site.register(Issue, IssueAdmin)