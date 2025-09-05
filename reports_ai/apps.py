from pathlib import Path

from django.apps import AppConfig


class ReportsAiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "reports_ai"
    # Compute the path from this file to avoid hardcoded absolute paths
    path = str(Path(__file__).resolve().parent)
