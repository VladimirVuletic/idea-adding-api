import subprocess

from app.core.settings import settings

def run_cmd(cmd, cwd):
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True
    )

    return result.stdout

def push_changes(commit_message):
    repo_path = settings.REPO_PATH

    output = []
    for git_cmd in [
        ['git', 'add', '.'],
        ['git', 'commit', '-m', commit_message],
        ['git', 'push']
    ]:
        output.append(run_cmd(git_cmd, repo_path))

    return output