
# Reports AI - Alpha

**Status: This project is in Alpha. APIs and features may change.**

Reports AI is a Django module that leverages the power of Large Language Models (LLMs) to automatically generate summary reports from your project's Git history. It provides a simple, yet powerful, interface within the Django admin to create, manage, and view these reports.

![Reports AI Screenshot](https://placehold.co/600x400)

## Features

- **Automated Report Generation**: Analyze your Git commit history and generate high-level summaries of development progress.
- **LLM Integration**: Powered by `django-ai-assistant`, it supports a wide range of LLM providers, including OpenAI, Anthropic, and Google.
- **Private Repository Support**: Securely access private GitHub repositories using a personal access token.
- **Django Admin Interface**: Manage and view reports directly from the Django admin.
- **Customizable**: Easily extendable to support different LLM providers and models.

## Installation

1.  **Install the package**:

    ```bash
    pip install -e git+https://github.com/fsecada01/reports_ai.git#egg=reports_ai
    ```

2.  **Add to `INSTALLED_APPS`**:

    In your project's `settings.py`, add `reports_ai` and `django_ai_assistant` to the `INSTALLED_APPS` list:

    ```python
    INSTALLED_APPS = [
        # ...
        'reports_ai',
        'django_ai_assistant',
    ]
    ```

3.  **Run migrations**:

    ```bash
    python manage.py migrate
    ```

## Requirements

- Python 3.11+
- Django 4.2+

## Configuration

1.  **Environment Variables**:

    Create a `.env` file in your project's root directory and add the following variables:

    ```
    # .env
    REPORTS_AI_LLM_PROVIDER=openai
    REPORTS_AI_LLM_API_KEY=your_api_key
    # Optional: override model (default: gpt-4o)
    REPORTS_AI_LLM_MODEL=gpt-4o
    REPORTS_AI_GITHUB_TOKEN=your_github_token
    ```

2.  **`settings.py`**:

    Add the following to your `settings.py` to configure the LLM provider and clone path:

    ```python
    # settings.py
    REPORTS_AI_CLONE_PATH = "git_repos"

    LLM_PROVIDER = os.getenv('REPORTS_AI_LLM_PROVIDER', 'openai')
    LLM_API_KEY = os.getenv('REPORTS_AI_LLM_API_KEY')

    if LLM_PROVIDER == 'openai':
        os.environ['OPENAI_API_KEY'] = LLM_API_KEY
    elif LLM_PROVIDER == 'anthropic':
        os.environ['ANTHROPIC_API_KEY'] = LLM_API_KEY
    elif LLM_PROVIDER == 'google':
        os.environ['GOOGLE_API_KEY'] = LLM_API_KEY
    ```

### Providers and required packages

`reports_ai` uses LangChain chat models under the hood. Depending on `REPORTS_AI_LLM_PROVIDER`, ensure the corresponding package is installed:

- `openai` (default): `langchain-openai` (already included via dependency tree)
- `anthropic`: install `langchain-anthropic`
- `google` (Gemini): install `langchain-google-genai`

Example with `uv`:

```bash
uv add langchain-anthropic  # or langchain-google-genai
```

## Usage

1.  **Navigate to the Django Admin**:

    Go to your Django admin interface and you will see a "Report Instances" section.

2.  **Create a Report Instance**:

    -   Click "Add Report Instance".
    -   Fill in the title and the URL of the Git repository.
    -   Save the instance.

3.  **Generate a Report**:

    -   From the report instance detail view, click the "Generate/Regenerate Report" button.
    -   The report generation will be queued as a background task.
    -   The status of the report will be updated to "Generating" and then "Completed" or "Failed".

4.  **View the Report**:

    -   Once the report is completed, the generated summary will be displayed in the report instance detail view.

## Customization

### Supported LLM Providers

This module supports OpenAI, Anthropic, and Google out of the box. To add a new provider, you need to:

1.  Update the `settings.py` to set the provider-specific API key.
2.  Update `reports_ai/ai_assistants.py` to include the new provider and model.

### Report Generation Prompt

You can customize the prompt used for report generation by modifying the `instructions` in the `ReportAssistant` class in `reports_ai/ai_assistants.py`.

## Development: Pre-commit hooks

Install and run pre-commit to keep code formatted and linted consistently:

```bash
uv sync --dev
pre-commit install
pre-commit run --all-files
```

## Releasing

We use tag-driven releases. To cut a release:

- Update version in `pyproject.toml` (`[project].version`).
- Commit the change, then create and push a tag:

```bash
git commit -am "chore(release): vX.Y.Z"
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z
```

CI will build artifacts, create a GitHub Release, and publish to PyPI (requires `PYPI_API_TOKEN` secret). See CONTRIBUTING.md for details.
