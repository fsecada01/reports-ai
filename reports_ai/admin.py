from django.contrib import admin
from django.urls import path

from .models import ReportInstance
from .views import (
    ReportInstanceCreateView,
    ReportInstanceDetailView,
    ReportInstanceListView,
    trigger_report_generation,
)


@admin.register(ReportInstance)
class ReportInstanceAdmin(admin.ModelAdmin):
    list_display = ("title", "git_repo_url", "report_status", "created_at")
    list_filter = ("report_status",)
    search_fields = (
        "title",
        "git_repo_url",
    )

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "reports/",
                self.admin_site.admin_view(ReportInstanceListView.as_view()),
                name="reports_ai_reportinstance_list",
            ),
            path(
                "reports/create/",
                self.admin_site.admin_view(ReportInstanceCreateView.as_view()),
                name="reports_ai_reportinstance_add",
            ),
            path(
                "reports/<int:pk>/",
                self.admin_site.admin_view(ReportInstanceDetailView.as_view()),
                name="reports_ai_reportinstance_change",
            ),
            path(
                "reports/<int:pk>/generate/",
                self.admin_site.admin_view(trigger_report_generation),
                name="generate_report",
            ),
        ]
        return my_urls + urls
