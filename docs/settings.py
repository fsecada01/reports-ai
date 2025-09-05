import os

DEBUG = True

SECRET_KEY = "a-very-secret-key"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "reports_ai",
    "django_ai_assistant",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

STATIC_URL = "/static/"

# REPORTS_AI_CLONE_PATH setting for GitService
REPORTS_AI_CLONE_PATH = os.path.join(os.path.dirname(__file__), "cloned_repos")

# LLM Configuration (for pdoc to import the module without errors)
LLM_PROVIDER = os.getenv("REPORTS_AI_LLM_PROVIDER", "openai")
LLM_API_KEY = os.getenv("REPORTS_AI_LLM_API_KEY", "dummy_key")
LLM_MODEL = os.getenv("REPORTS_AI_LLM_MODEL", "gpt-4o")

if LLM_PROVIDER == "openai":
    os.environ["OPENAI_API_KEY"] = LLM_API_KEY
elif LLM_PROVIDER == "anthropic":
    os.environ["ANTHROPIC_API_KEY"] = LLM_API_KEY
elif LLM_PROVIDER == "google":
    os.environ["GOOGLE_API_KEY"] = LLM_API_KEY
