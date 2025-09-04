
from celery import shared_task
from django.conf import settings
from .models import ReportInstance
from .services.llm_service import LLMService
from .services.git_service import GitService

@shared_task
def generate_report_task(report_instance_id: int):
    """A Celery task to generate a report from a ReportInstance."""
    try:
        report_instance = ReportInstance.objects.get(pk=report_instance_id)
        report_instance.report_status = 'generating'
        report_instance.save()

        token = getattr(settings, 'REPORTS_AI_GITHUB_TOKEN', None)
        git_service = GitService(repo_url=report_instance.git_repo_url, token=token)

        llm_service = LLMService(repo_path=git_service.clone_path)
        summary = llm_service.generate_summary(last_commit_hash=report_instance.last_commit_hash)

        report_instance.generated_report = summary
        report_instance.last_commit_hash = git_service.get_current_head()
        report_instance.report_status = 'completed'
        report_instance.save()

    except ReportInstance.DoesNotExist:
        # Handle case where ReportInstance is not found
        # You might want to log this error
        pass
    except Exception as e:
        # Handle other exceptions and update status to 'failed'
        if 'report_instance' in locals():
            report_instance.report_status = 'failed'
            report_instance.save()
        # You might want to log the exception e
        pass
