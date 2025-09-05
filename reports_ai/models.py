# reports_ai/models.py
from django.db import models


class ReportInstance(models.Model):
    REPORT_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("generating", "Generating"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    )
    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=50, default="investor_update")
    git_repo_url = models.URLField(max_length=255)
    last_commit_hash = models.CharField(max_length=40, blank=True, null=True)
    generated_report = models.TextField(blank=True, null=True)
    report_status = models.CharField(
        max_length=20, choices=REPORT_STATUS_CHOICES, default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.get_report_status_display()})"
