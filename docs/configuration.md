# [Home](./index.html) | [API](./reports_ai.html)

# Installation & Configuration

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

## Configuration

### Environment Variables

Create a `.env` file in your project's root directory and add the following variables:

```
# .env
REPORTS_AI_LLM_PROVIDER=openai
REPORTS_AI_LLM_API_KEY=your_api_key
REPORTS_AI_GITHUB_TOKEN=your_github_token
```

-   `REPORTS_AI_LLM_PROVIDER`: The LLM provider to use. Supported providers are `openai`, `anthropic`, and `google`.
-   `REPORTS_AI_LLM_API_KEY`: Your API key for the selected LLM provider.
-   `REPORTS_AI_GITHUB_TOKEN`: Your GitHub personal access token for accessing private repositories.

### `settings.py`

Add the following to your `settings.py`:

```python
# settings.py
import os

# Path where the git repositories will be cloned
REPORTS_AI_CLONE_PATH = "git_repos"

# LLM Configuration
LLM_PROVIDER = os.getenv('REPORTS_AI_LLM_PROVIDER', 'openai')
LLM_API_KEY = os.getenv('REPORTS_AI_LLM_API_KEY')
LLM_MODEL = os.getenv('REPORTS_AI_LLM_MODEL', 'gpt-4o') # Optional: specify a model

# Set provider-specific environment variables
if LLM_PROVIDER == 'openai':
    os.environ['OPENAI_API_KEY'] = LLM_API_KEY
elif LLM_PROVIDER == 'anthropic':
    os.environ['ANTHROPIC_API_KEY'] = LLM_API_KEY
elif LLM_PROVIDER == 'google':
    os.environ['GOOGLE_API_KEY'] = LLM_API_KEY
```

### `ai_assistants.py`

Create an `ai_assistants.py` file in your `reports_ai` app directory:

```python
# reports_ai/ai_assistants.py
from django.conf import settings
from django_ai_assistant.assistant import Assistant
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

class ReportAssistant(Assistant):
    id = "report_assistant"
    name = "Report Assistant"
    instructions = "You are an expert software development project manager..."

    def get_llm(self):
        provider = settings.LLM_PROVIDER
        model = getattr(settings, 'LLM_MODEL', None)

        if provider == 'openai':
            return ChatOpenAI(model=model or 'gpt-4o')
        elif provider == 'anthropic':
            return ChatAnthropic(model=model or 'claude-3-opus-20240229')
        elif provider == 'google':
            return ChatGoogleGenerativeAI(model=model or 'gemini-pro')
        else:
            # Default to OpenAI if provider is not recognized
            return ChatOpenAI(model=model or 'gpt-4o')
```
