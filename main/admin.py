# main/admin.py
from django.urls import path, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import admin
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Issue, Profile, Feedback
from django.utils.html import format_html
from .forms import ProgressReportForm

# Define the admin interface for the Feedback model
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('issue', 'content', 'created_at')  # Fields to display in the admin list view
    list_filter = ('issue', 'user')  # Fields to filter the list view

# Define the admin interface for the Issue model
class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'issue', 'category', 'ward', 'status', 'image', 'reported_by', 'created_at', 'address', 'view_progress_report_button')
    list_filter = ('status', 'ward', 'category')
    search_fields = ('issue', 'ward', 'reported_by__username', 'category')
    actions = ['mark_as_in_progress', 'mark_as_resolved', 'mark_as_pending']
    
    def view_progress_report_button(self, obj):
        url = reverse('admin:view_progress_report', args=[obj.id])
        return format_html('<a class="button" href="{}">Progress Report</a>', url)

    view_progress_report_button.short_description = 'Progress Report'
    view_progress_report_button.allow_tags = True

    def view_progress_report(self, request, obj_id):
        issue = Issue.objects.get(id=obj_id)
        if request.method == 'POST':
            form = ProgressReportForm(request.POST)
            if form.is_valid():
                progress_report = form.cleaned_data['progress_report']
                status = form.cleaned_data['status']
                issue.status = status
                issue.progress_report = progress_report
                issue.save()
                Feedback.objects.create(issue=issue, content=progress_report, user=request.user)
                self.send_issue_update([issue])
                return redirect('admin:main_issue_changelist')  # Redirect to admin issues list

        form = ProgressReportForm(initial={'progress_report': issue.progress_report, 'status': issue.status})
        return render(request, 'progress_report.html', {'issue': issue, 'form': form})

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
                path('progress_report/<int:obj_id>/', self.admin_site.admin_view(self.view_progress_report), name='view_progress_report'),
        ]
        return custom_urls + urls

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
                "status": issue.status,
                "progress_report": issue.progress_report or "",
                "address": issue.address or "",
            }
        )

admin.site.register(Issue, IssueAdmin)
admin.site.register(Profile)
admin.site.register(Feedback, FeedbackAdmin)