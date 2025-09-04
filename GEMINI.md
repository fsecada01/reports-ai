# Architect and Bootstrap a Django Report Module with LLM and Git Integration

## Objective

Act as a senior software architect and full-stack developer. Your task is to plan, architect, and provide an implementation plan for a new Django module named `reports_ai`. This module will generate summary reports by analyzing Git commit history and leveraging a Large Language Model (LLM).

## Context

-   **Project**: An existing Django project with a modular architecture.
-   **Target Module**: `reports_ai`, a self-contained Django app.
-   **Key Dependencies**:
    -   **GitPython**: For reading Git commit histories.
    -   **Celery**: For running background report generation tasks.
    -   **LangChain (or similar SDK)**: For interacting with an LLM.
-   **Future Expansion**: The design should allow for future integration of advanced NLP and ML techniques to improve report accuracy and quality.

## 1. Persona and Goal

-   **Persona**: A senior software architect specializing in Django and AI integrations. The goal is to provide a comprehensive, step-by-step plan for building the `reports_ai` module. The plan should be modular, scalable, and easy to understand.
-   **Goal**: Provide the following in a structured, Markdown format:
    -   High-level architecture diagram (text-based).
    -   Detailed Django app structure (`reports_ai` directory).
    -   Key model definitions (`reports_ai/models.py`).
    -   Service layer design (`reports_ai/services.py`).
    -   Celery task implementation (`reports_ai/tasks.py`).
    -   Views and URL routing (`reports_ai/views.py`, `reports_ai/urls.py`).
    -   Future state roadmap for ML/NLP integration.

## 2. Architectural Overview

Generate a high-level, text-based diagram illustrating the interaction between the user, the Django application, the Git repository, the task queue, and the LLM.

**Diagram:**

```text
[Web Frontend] -> [Django Views]
      |
      v
[Celery Task] -> [Git Service] -> [Git Repo]
      |
      v
[LLM Service] -> [LLM API]
      |
      v
[Celery Task] -> [Django Model (ReportInstance)]
      ^
      |
[Web Frontend (Report View)]
```

---

## 3. Implementation Plan

### 3.1. Django App Structure

```text
reports_ai/
├── migrations/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── urls.py
├── views.py
├── forms.py
├── tasks.py
└── services/
    ├── __init__.py
    ├── git_service.py
    └── llm_service.py
```

### 3.2. Models (`reports_ai/models.py`)

Provide detailed code for the `ReportInstance` model, including fields for state management and future expansion. Use Django's `choices` for `report_status` to ensure data integrity.

```python
# reports_ai/models.py
from django.db import models

class ReportInstance(models.Model):
    REPORT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('generating', 'Generating'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=50, default='investor_update')
    git_repo_path = models.CharField(max_length=255)
    last_commit_hash = models.CharField(max_length=40, blank=True, null=True)
    generated_report = models.TextField(blank=True, null=True)
    report_status = models.CharField(
        max_length=20,
        choices=REPORT_STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_report_status_display()})"
```

### 3.3. Services (`reports_ai/services/`)

-   **`git_service.py`**:
    -   Define a class `GitService` to handle Git interactions.
    -   Implement `get_commits_since()` to fetch commits and `get_current_head()` to get the latest commit hash.
    -   Include error handling for invalid Git repositories or paths.
-   **`llm_service.py`**:
    -   Define a class `LLMService`.
    -   Implement `generate_summary()` to send commit logs to the LLM API and return the summary.
    -   Provide a default, well-structured prompt that can be customized.

### 3.4. Celery Tasks (`reports_ai/tasks.py`)

-   **`generate_report_task()`**:
    -   Create a Celery task that takes a `ReportInstance` ID.
    -   Inside the task:
        1.  Fetch the `ReportInstance`.
        2.  Update status to `'generating'`.
        3.  Call `GitService` to get commit history.
        4.  Call `LLMService` to generate the report.
        5.  Save the generated report and update `last_commit_hash`.
        6.  Update status to `'completed'` or `'failed'`.

### 3.5. Views and URLs (`reports_ai/views.py`, `reports_ai/urls.py`)

-   **`ReportCreateView`**: A class-based view to create a new `ReportInstance`. Use a `ModelForm` based on the `ReportInstance` model.
-   **`ReportListView`**: A view to list all reports with their status.
-   **`ReportDetailView`**: A view to display the generated report content. Include a button to trigger the `generate_report_task` for a specific report instance.
-   Define the necessary URL patterns for these views.

### 3.6. Future State Roadmap (ML/NLP Integration)

Use this section to brainstorm potential enhancements and how they would fit into the existing architecture.

-   **Named Entity Recognition (NER)**: Use NLP to identify key entities in commit messages (e.g., ticket numbers, developer names). This can enrich the prompt sent to the LLM.
-   **Sentiment Analysis**: Analyze commit message sentiment to gauge overall team morale or project momentum.
-   **Topic Modeling**: Identify major topics or themes in commit histories (e.g., "Bug Fixes," "Feature Development") to produce more structured reports.
-   **Retrieval-Augmented Generation (RAG)**: For more complex or historical reports, use commit data and vector databases to retrieve relevant code snippets or documentation, providing more context to the LLM.

## 4. Final Request

Provide the complete Python code for the `ReportInstance` model, the `git_service.py`, and the `generate_report_task` based on the design specified above. Include comments explaining the logic and error handling. For the LLM service, provide a generic implementation that can be easily configured with an actual API endpoint.