from __future__ import annotations

import os
from typing import Optional

from django_ai_assistant import AIAssistant, method_tool

from .services.git_service import GitService


class ReportAssistant(AIAssistant):
    """AI assistant specialized in summarizing Git commit history.

    Exposes a `get_commits` tool that fetches commit messages from the
    repository path passed during initialization.
    """

    id = "report_assistant"
    name = "Report Assistant"
    instructions = (
        "You summarize recent Git commits into concise progress notes. "
        "When needed, call the get_commits tool to retrieve commit messages."
    )
    model = os.getenv("REPORTS_AI_LLM_MODEL", "gpt-4o")
    temperature: float | None = 0.3

    # Provider-aware LLM selection. Defaults to OpenAI via langchain_openai.
    def get_llm(self):  # type: ignore[override]
        provider = (
            os.getenv("REPORTS_AI_LLM_PROVIDER")
            or os.getenv("LLM_PROVIDER")
            or "openai"
        ).lower()
        model = self.get_model()
        temperature = self.get_temperature()
        model_kwargs = self.get_model_kwargs()

        def _merge_kwargs(base: dict):
            if temperature is not None:
                base["temperature"] = temperature
            if model_kwargs:
                base["model_kwargs"] = model_kwargs
            return base

        if provider in {"openai", "oai"}:
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(**_merge_kwargs({"model": model}))
        elif provider in {"anthropic"}:
            try:
                from langchain_anthropic import ChatAnthropic
            except ImportError as exc:
                raise ImportError(
                    "Provider 'anthropic' selected but 'langchain-anthropic' is not installed.\n"
                    "Install it (e.g., 'uv add langchain-anthropic' or 'pip install langchain-anthropic')."
                ) from exc
            return ChatAnthropic(**_merge_kwargs({"model": model}))
        elif provider in {"google", "gemini"}:
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
            except ImportError as exc:
                raise ImportError(
                    "Provider 'google' selected but 'langchain-google-genai' is not installed.\n"
                    "Install it (e.g., 'uv add langchain-google-genai' or 'pip install langchain-google-genai')."
                ) from exc
            return ChatGoogleGenerativeAI(**_merge_kwargs({"model": model}))
        else:
            raise ValueError(
                f"Unsupported REPORTS_AI_LLM_PROVIDER: {provider!r}. Supported: openai, anthropic, google."
            )

    @method_tool
    def get_commits(self, since: Optional[str] = None) -> list[str]:
        """Return commit messages since a given commit hash (or all commits).

        Args:
            since: Optional commit hash to filter the log.

        Returns:
            A list of commit message strings.
        """
        repo_path = self._init_kwargs.get("repo_path")
        service = GitService(repo_path=repo_path)
        commits = service.get_commits_since(since)
        return [c.message for c in commits]
