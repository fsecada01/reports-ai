from django_ai.assistant import Assistant
from .git_service import GitService

class LLMService:
    """A service for interacting with a Large Language Model using django-ai-assistant."""

    def __init__(self, repo_path: str):
        """Initializes the LLMService.

        Args:
            repo_path: The path to the Git repository.
        """
        self.repo_path = repo_path
        self.assistant = Assistant()
        self.assistant.register_tool(self.get_commits)

    def get_commits(self, since: str = None) -> list[str]:
        """Gets all commits since a given commit hash, or all commits if since is None."""
        git_service = GitService(repo_path=self.repo_path)
        commits = git_service.get_commits_since(since)
        return [commit.message for commit in commits]

    def generate_summary(self, last_commit_hash: str = None) -> str:
        """Generates a summary of the git commits.

        Args:
            last_commit_hash: The commit hash to get commits since.

        Returns:
            The generated summary.
        """
        prompt = (
            "Please provide a summary of the git commits. "
            "If a commit hash is provided, summarize the commits since that hash."
        )
        if last_commit_hash:
            prompt += f" The last commit hash is {last_commit_hash}."
        
        return self.assistant.run(prompt)