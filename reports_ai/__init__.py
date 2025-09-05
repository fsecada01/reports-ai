"""reports_ai: AI-assisted summaries from Git history for Django.

This package provides:
- A `ReportAssistant` (LLM-backed) to summarize recent commits.
- Admin actions and a background task to generate reports.
- Minimal services to interact with Git repositories.

See the Guides and Configuration pages for setup and usage.
"""

# Intentionally do not constrain __all__ so documentation and explorers
# can see submodules and objects. Pdoc will surface submodules under
# the package page automatically.
