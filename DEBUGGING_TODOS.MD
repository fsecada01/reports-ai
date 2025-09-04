# DEBUGGING_TODOS.MD

## Current Task: Generate API Documentation via `pdoc`

**Goal:** The primary goal is to successfully generate API documentation for the `reports_ai` Django module using `pdoc`.

**Current Problem:** When attempting to run `pdoc`, the process fails with the following error:

```
ModuleNotFoundError: No module named 'django_ai_assistant.assistant'
```

This error occurs specifically when `pdoc` tries to import `reports_ai.services.llm_service`, which in turn imports `Assistant` from `django_ai_assistant.assistant`.

## Context & Setup:

*   **Application:** `reports_ai` is a Django application designed to generate summary reports from Git history using LLMs.
*   **Dependencies:**
    *   `django-ai-assistant`: Used for LLM integrations. Installed via `uv`.
    *   `pdoc`: Used for API documentation generation. Installed via `uv`.
*   **Django Settings for `pdoc`:** A minimal `docs/settings.py` file is used to configure Django settings for `pdoc`'s execution. This file includes `reports_ai` and `django_ai_assistant` in `INSTALLED_APPS`.
*   **Execution Script:** A Python script, `run_pdoc.py`, is used to execute `pdoc`. This script sets the `DJANGO_SETTINGS_MODULE` environment variable and calls `django.setup()` before invoking `pdoc.pdoc()`.

## Steps Taken & Observations (Chronological):

1.  **Initial `pdoc` attempts:** Failed with `django.core.exceptions.ImproperlyConfigured: Requested setting INSTALLED_APPS, but settings are not configured.`
    *   **Action:** Created `docs/settings.py` and set `DJANGO_SETTINGS_MODULE`.

2.  **Subsequent `pdoc` attempts:** Failed with `django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.`
    *   **Action:** Added `django.setup()` to `run_pdoc.py`.

3.  **Next `pdoc` attempts:** Failed with `django.core.exceptions.ImproperlyConfigured: The app module <module 'reports_ai' (namespace) from [...]> has multiple filesystem locations.`
    *   **Observation:** This was due to `reports_ai` being installed in editable mode (`uv pip install -e .[dev]`) and also being present in the current directory. Django was finding it in both `site-packages` and the local directory.
    *   **Action:** Uninstalled `reports-ai` (editable), reinstalled it as a regular package (`uv pip install .[dev,doc]`), and explicitly defined the `path` attribute in `reports_ai/apps.py`.

4.  **Current `pdoc` attempts:** Consistently fail with `ModuleNotFoundError: No module named 'django_ai_assistant.assistant'`.
    *   **Observation 1:** `django-ai-assistant` is confirmed to be installed (`uv pip list` shows `django-ai-assistant 0.1.2`).
    *   **Observation 2:** The installation location is `C:\dev\python\modules\reports_ai\.venv\Lib\site-packages\django_ai_assistant`.
    *   **Observation 3:** Inspection of the `django_ai_assistant` directory (`list_directory`) shows no `assistant.py` file directly under it. Subdirectories include `api`, `helpers`, `langchain`, `management`, `migrations`.
    *   **Hypothesis:** The `Assistant` class is likely located in a different submodule within the `django_ai_assistant` package than `django_ai_assistant.assistant` suggests.

## Previous Task Requests (Context for Triage):

Before encountering this persistent `pdoc` issue, the following tasks were being worked on and are largely complete, but the documentation generation is the final hurdle:

*   **Architect and bootstrap a Django report module with LLM and Git integration.**
    *   This involved planning, architecting, and implementing the `reports_ai` Django app.
    *   Key components implemented: `models.py`, `services/git_service.py`, `services/llm_service.py`, `tasks.py`, `forms.py`, `admin.py`, `views.py`, `urls.py`, and Django admin templates.
    *   **Specific LLM Integration:** Switched from `langchain` to `django-ai-assistant` as the LLM integration library.
    *   **GitHub Token Feature:** Implemented support for accessing private GitHub repositories using a token.
    *   **Environment Variable Management:** Integrated `python-dotenv` for loading sensitive values from `.env` files.
    *   **Provider-Agnostic LLM Configuration:** Implemented a mechanism to configure LLM providers (OpenAI, Anthropic, Google) via environment variables.

*   **Generate a UI-first `README.MD` file that is detailed and contains informative instructions on how to use and customize it for workflows.**
    *   **Status:** Completed.

*   **Generate doc pages to detail key sections of the application.**
    *   **Status:** Completed (`docs/index.md`, `docs/configuration.md`, `docs/usage.md`).

*   **Declare that this application is in Alpha.**
    *   **Status:** Included in `README.md` and `docs/index.md`.

**The primary remaining issue is resolving the `ModuleNotFoundError` to successfully generate the `pdoc` API documentation.**
