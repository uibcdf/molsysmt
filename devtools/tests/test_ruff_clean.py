import subprocess
from pathlib import Path

def test_ruff_clean_across_repo():
    """Verify that ruff check passes with zero errors on molsysmt including forms and third_party."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    res = subprocess.run(
        ["ruff", "check", "--no-cache", "molsysmt"],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, f"Ruff check failed with output:\n{res.stdout}\n{res.stderr}"
