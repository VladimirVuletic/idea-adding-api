from app.services.idea_service import run_cmd

def test_run_cmd():
    cmd = ["cmd", "/c", "echo", "Something"]
    cwd = f"C:\\Python projects\\idea-adding-api"

    assert run_cmd(cmd, cwd) == "Something\n"

