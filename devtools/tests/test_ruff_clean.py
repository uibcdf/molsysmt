import subprocess
from pathlib import Path


def test_ruff_clean_across_repo():
    """Run the configured Ruff boundary; legacy paths are tracked by #212."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    res = subprocess.run(
        ["ruff", "check", "--no-cache", "--force-exclude", "."],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, (
        f"Ruff check failed with output:\n{res.stdout}\n{res.stderr}"
    )


def test_core_critical_ruff_rules():
    """Keep the legacy core protected while its full baseline is migrated."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    res = subprocess.run(
        [
            "ruff",
            "check",
            "--no-cache",
            "--select",
            "F821,F822,F823,B006,B023",
            "molsysmt",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, (
        f"Critical core Ruff check failed:\n{res.stdout}\n{res.stderr}"
    )
