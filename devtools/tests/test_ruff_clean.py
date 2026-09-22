import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def test_ruff_selects_complete_core():
    """Keep every Python source file under the default Ruff gate."""
    selected = subprocess.run(
        ["ruff", "check", "--show-files", "."],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert selected.returncode == 0, selected.stderr
    checked_files = {
        Path(filename).resolve()
        for filename in selected.stdout.splitlines()
        if filename
    }
    tracked = subprocess.run(
        ["git", "ls-files", "--cached", "--", "molsysmt"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    expected = {
        REPO_ROOT / filename
        for filename in tracked.stdout.splitlines()
        if filename.endswith(".py")
    }
    expected.add(REPO_ROOT / "devtools/scripts/validate_devguide.py")
    expected.add(REPO_ROOT / "molsysviewer_molsysmt/addon.py")
    assert expected <= checked_files, sorted(
        str(path) for path in expected - checked_files
    )


def test_ruff_clean_across_repo():
    """Check lint and format for every selected Python file."""
    for command in (
        ["ruff", "check", "--no-cache", "."],
        ["ruff", "format", "--check", "."],
    ):
        result = subprocess.run(command, cwd=REPO_ROOT, capture_output=True, text=True)
        assert result.returncode == 0, (
            f"{' '.join(command)} failed:\n{result.stdout}\n{result.stderr}"
        )
