import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MIGRATED_PATHS = (
    (REPO_ROOT / "devtools/ruff_migrated_paths.txt").read_text().splitlines()
)


def test_ruff_clean_across_repo():
    """Run the configured Ruff boundary; legacy paths are tracked by #212."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    selected = subprocess.run(
        ["ruff", "check", "--show-files", "."],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    assert selected.returncode == 0, selected.stderr
    checked_files = {
        Path(filename).resolve().relative_to(repo_root).as_posix()
        for filename in selected.stdout.splitlines()
        if filename.strip()
    }
    expected = {
        "devtools/scripts/validate_devguide.py",
        "molsysviewer_molsysmt/addon.py",
    }
    assert expected <= checked_files, (
        f"Ruff must inspect the maintained tooling and add-on; "
        f"missing {sorted(expected - checked_files)}"
    )
    res = subprocess.run(
        ["ruff", "check", "--no-cache", "."],
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


def test_migrated_paths_manifest():
    """Keep the migrated subtrees explicit during issue #212."""
    assert {
        "molsysmt/_private",
        "molsysmt/attribute",
        "molsysmt/form",
        "molsysmt/lib",
    } <= set(MIGRATED_PATHS)
    assert len(MIGRATED_PATHS) == len(set(MIGRATED_PATHS))
    assert all(path.startswith("molsysmt/") for path in MIGRATED_PATHS)
    assert all((REPO_ROOT / path).is_dir() for path in MIGRATED_PATHS)


@pytest.mark.parametrize("package_path", MIGRATED_PATHS)
def test_migrated_package_ruff_gate(package_path):
    """Keep every Python file in each migrated package under Ruff."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    package_dir = repo_root / package_path
    expected = {path.resolve() for path in package_dir.rglob("*.py")}
    selected = subprocess.run(
        ["ruff", "check", "--show-files", package_path],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    assert selected.returncode == 0, selected.stderr
    checked = {Path(filename).resolve() for filename in selected.stdout.splitlines()}
    assert expected and checked == expected, (
        f"Ruff selected {sorted(str(path) for path in checked)}; "
        f"expected {sorted(str(path) for path in expected)}"
    )

    for command in (
        ["ruff", "check", "--no-cache", package_path],
        ["ruff", "format", "--check", package_path],
    ):
        result = subprocess.run(command, cwd=repo_root, capture_output=True, text=True)
        assert result.returncode == 0, (
            f"{' '.join(command)} failed:\n{result.stdout}\n{result.stderr}"
        )
