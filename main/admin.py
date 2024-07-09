# main/admin.py
from django.contrib import admin
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Issue, Profile, Feedback

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('issue', 'content', 'created_at')
    list_filter = ('issue', 'user')

class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'issue', 'ward', 'status', 'reporter', 'image', 'created_at')
    list_filter = ('status', 'ward')
    search_fields = ('issue', 'ward') 
    actions = ['mark_as_in_progress', 'mark_as_resolved', 'mark_as_pending']

    def mark_as_in_progress(self, request, queryset):
        queryset.update(status='In Progress')
        self.send_issue_update(queryset)

    def mark_as_resolved(self, request, queryset):
        queryset.update(status='Resolved')
        self.send_issue_update(queryset)

    def mark_as_pending(self, request, queryset):
        queryset.update(status='Pending')
        self.send_issue_update(queryset)

    def send_issue_update(self, queryset):
        channel_layer = get_channel_layer()
        for issue in queryset:
            async_to_sync(channel_layer.group_send)(
                "issue_updates", 
                {
                    "type": "issue.update", 
                    "issue_id": issue.id, 
                    "status": issue.status
                }
            )

admin.site.register(Issue, IssueAdmin)
admin.site.register(Profile)
admin.site.register(Feedback, FeedbackAdmin)