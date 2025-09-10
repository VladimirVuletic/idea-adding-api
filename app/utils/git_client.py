import subprocess

from app.core.settings import settings


class GitClient:
    def __init__(self, repo_path: str = None):
        self.repo_path = repo_path if repo_path else settings.REPO_PATH

    def _run_cmd(self, cmd, cwd):
        result = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, check=True
        )

        return result.stdout

    def push_changes(self, commit_message):
        output = []
        for git_cmd in [
            ["git", "add", "."],
            ["git", "commit", "-m", commit_message],
            ["git", "push"],
        ]:
            output.append(self._run_cmd(git_cmd, self.repo_path))

        return output
