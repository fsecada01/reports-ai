import git
import os
from django.conf import settings
from urllib.parse import urlparse

class GitService:
    """A service for interacting with Git repositories."""

    def __init__(self, repo_url: str, token: str = None):
        """Initializes the GitService.

        Args:
            repo_url: The URL of the Git repository.
            token: The GitHub token for private repositories.
        """
        self.repo_url = repo_url
        self.token = token
        self.clone_path = self._get_clone_path()
        self.repo = self._get_or_clone_repo()

    def _get_clone_path(self) -> str:
        """Gets the local path to clone the repository to."""
        clone_base_path = getattr(settings, 'REPORTS_AI_CLONE_PATH', 'git_repos')
        repo_name = os.path.splitext(os.path.basename(urlparse(self.repo_url).path))[0]
        return os.path.join(clone_base_path, repo_name)

    def _get_or_clone_repo(self) -> git.Repo:
        """Gets the repository from the local path, or clones it if it doesn't exist."""
        if os.path.exists(self.clone_path):
            repo = git.Repo(self.clone_path)
            repo.remotes.origin.pull()
            return repo
        else:
            if self.token:
                clone_url = self.repo_url.replace('https://', f"https://{self.token}@")
            else:
                clone_url = self.repo_url
            return git.Repo.clone_from(clone_url, self.clone_path)

    def get_current_head(self) -> str:
        """Gets the current HEAD commit hash."""
        return self.repo.head.commit.hexsha

    def get_commits_since(self, last_commit_hash: str | None) -> list[git.Commit]:
        """Gets all commits since a given commit hash."""
        if last_commit_hash:
            return list(self.repo.iter_commits(f"{last_commit_hash}..HEAD"))
        return list(self.repo.iter_commits())