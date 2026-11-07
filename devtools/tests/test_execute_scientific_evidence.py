import subprocess
from pathlib import Path

import pytest

from devtools.scripts.execute_scientific_evidence import execute_nodes

REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize(
    ("body", "expected_verdict", "expected_counts"),
    [
        ("assert 2 + 2 == 4", True, {"passed": 1, "skipped": 0, "failures": 0}),
        ("assert 2 + 2 == 5", False, {"passed": 0, "skipped": 0, "failures": 1}),
        (
            "pytest.skip('missing oracle')",
            False,
            {"passed": 0, "skipped": 1, "failures": 0},
        ),
    ],
)
def test_execution_certificate_rejects_failures_and_skips(
    tmp_path, body, expected_verdict, expected_counts
):
    test_file = tmp_path / "test_evidence.py"
    test_file.write_text(f"import pytest\n\ndef test_evidence():\n    {body}\n")
    certificate_path = tmp_path / "certificate.json"

    verdict, certificate = execute_nodes(
        ["test_evidence.py::test_evidence"],
        repo_root=tmp_path,
        receptor="llm",
        certificate_path=certificate_path,
    )

    assert verdict is expected_verdict
    assert certificate_path.is_file()
    for field, value in expected_counts.items():
        assert certificate[field] == value
    assert certificate["registered_nodes"] == 1
    assert certificate["collected_cases"] == 1


def test_execution_certificate_rejects_an_uncollectable_node(tmp_path):
    Path(tmp_path / "test_evidence.py").write_text(
        "def test_other():\n    assert True\n", encoding="utf-8"
    )

    verdict, certificate = execute_nodes(
        ["test_evidence.py::test_missing"],
        repo_root=tmp_path,
        receptor="llm",
    )

    assert verdict is False
    assert certificate["pytest_exit_code"] != 0
    assert certificate["collected_cases"] == 0


def test_release_certificate_requires_a_clean_git_commit(tmp_path, monkeypatch):
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path.parent))
    Path(tmp_path / "test_evidence.py").write_text(
        "def test_evidence():\n    assert 2 + 2 == 4\n", encoding="utf-8"
    )

    verdict, certificate = execute_nodes(
        ["test_evidence.py::test_evidence"],
        repo_root=tmp_path,
        receptor="llm",
        require_clean=True,
    )

    assert verdict is False
    assert certificate["passed"] == 1
    assert certificate["tracked_source_dirty"] is None
    assert certificate["release_eligible"] is False


def test_heavy_release_workflows_require_the_zero_skip_certificate():
    for relative_path in (
        ".github/workflows/ci-full.yaml",
        ".github/workflows/ci-weekly.yaml",
    ):
        workflow = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
        assert "execute_scientific_evidence.py" in workflow
        assert "--require-clean" in workflow
        assert "--certificate=scientific-evidence-certificate.json" in workflow


@pytest.fixture
def scientific_git_repo(tmp_path):
    """Use an actual independent commit, not a mocked clean Git response."""
    repo = tmp_path / "source"
    repo.mkdir()
    subprocess.run(["git", "init", "--quiet", str(repo)], check=True)
    for name, value in {
        "user.name": "Scientific source control",
        "user.email": "source-control@example.invalid",
        "commit.gpgsign": "false",
        "core.fsmonitor": "false",
    }.items():
        subprocess.run(["git", "config", name, value], cwd=repo, check=True)
    (repo / ".gitignore").write_text("__pycache__/\n.pytest_cache/\nbuild/\n")
    (repo / "test_evidence.py").write_text(
        "def test_evidence():\n    assert 2 + 2 == 4\n"
    )
    subprocess.run(
        ["git", "add", ".gitignore", "test_evidence.py"], cwd=repo, check=True
    )
    subprocess.run(
        ["git", "commit", "--quiet", "-m", "Scientific fixture [skip ci]"],
        cwd=repo,
        check=True,
    )
    return repo


@pytest.mark.parametrize("remove_after_loading", [False, True])
def test_release_certificate_rejects_an_actually_loaded_untracked_hook(
    scientific_git_repo, tmp_path, remove_after_loading
):
    repo = scientific_git_repo
    marker = tmp_path / "loaded-hook.txt"
    hook = repo / "conftest.py"
    hook.write_text(
        "from pathlib import Path\n"
        "def pytest_sessionstart(session):\n"
        f"    Path({str(marker)!r}).write_text('loaded')\n"
        + ("    Path(__file__).unlink()\n" if remove_after_loading else "")
    )
    verdict, certificate = execute_nodes(
        ["test_evidence.py::test_evidence"],
        repo_root=repo,
        require_clean=True,
    )
    assert marker.read_text() == "loaded"
    assert certificate["passed"] == 1
    assert certificate["tracked_source_dirty"] is False
    assert verdict is False
    assert certificate["release_eligible"] is False
    assert "conftest.py" in certificate["source_before"]["untracked_source_paths"]
    if remove_after_loading:
        assert certificate["source_after"]["untracked_source_paths"] == []


@pytest.mark.parametrize(
    "relative,contents",
    [
        ("helper.py", "VALUE = 1\n"),
        ("tests/data/reference.json", "{}\n"),
        ("tests/data/reference with spaces.npy", "reference\n"),
        ("pytest.ini", "[pytest]\n"),
        ("pyproject.toml", "[tool.pytest.ini_options]\n"),
        ("tests/scientific-evidence-certificate.json", "{}\n"),
    ],
)
def test_release_certificate_rejects_untracked_source_config_and_reference_inputs(
    scientific_git_repo, relative, contents
):
    path = scientific_git_repo / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents)
    verdict, certificate = execute_nodes(
        ["test_evidence.py::test_evidence"],
        repo_root=scientific_git_repo,
        require_clean=True,
    )
    assert certificate["passed"] == 1
    assert verdict is False
    assert certificate["tracked_source_dirty"] is False
    assert certificate["release_eligible"] is False
    assert relative in certificate["source_after"]["untracked_source_paths"]


@pytest.mark.parametrize(
    "artifact",
    [
        None,
        "scientific-evidence-certificate.json",
        "junit.xml",
        "coverage.xml",
        ".pytest-receptor/events.jsonl",
        "build/output.json",
    ],
)
def test_release_certificate_accepts_clean_source_and_reserved_workflow_artifacts(
    scientific_git_repo, artifact
):
    if artifact is not None:
        path = scientific_git_repo / artifact
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}\n")
    verdict, certificate = execute_nodes(
        ["test_evidence.py::test_evidence"],
        repo_root=scientific_git_repo,
        require_clean=True,
    )
    assert verdict is True
    assert certificate["release_eligible"] is True
    assert certificate["passed"] == 1


def test_release_certificate_rejects_a_commit_change_during_execution(
    scientific_git_repo,
):
    repo = scientific_git_repo
    (repo / "test_evidence.py").write_text(
        "import subprocess\nfrom pathlib import Path\n"
        "def test_evidence():\n"
        "    Path('new.txt').write_text('new source')\n"
        "    subprocess.run(['git', 'add', 'new.txt'], check=True)\n"
        "    subprocess.run(['git', 'commit', '--quiet', '-m', 'Changed source [skip ci]'], check=True)\n"
    )
    subprocess.run(["git", "add", "test_evidence.py"], cwd=repo, check=True)
    subprocess.run(
        ["git", "commit", "--quiet", "-m", "Source change control [skip ci]"],
        cwd=repo,
        check=True,
    )
    verdict, certificate = execute_nodes(
        ["test_evidence.py::test_evidence"],
        repo_root=repo,
        require_clean=True,
    )
    assert certificate["passed"] == 1
    assert certificate["tracked_source_dirty"] is False
    assert verdict is False
    assert certificate["release_eligible"] is False
    assert (
        certificate["source_before"]["commit"] != certificate["source_after"]["commit"]
    )


def test_release_certificate_rejects_tracked_input_restored_during_execution(
    scientific_git_repo,
):
    repo = scientific_git_repo
    original = (repo / "test_evidence.py").read_text()
    (repo / "test_evidence.py").write_text(
        "from pathlib import Path\n"
        "def test_evidence():\n"
        f'    Path("test_evidence.py").write_text({original!r})\n'
        "    assert 2 + 2 == 4\n"
    )
    verdict, certificate = execute_nodes(
        ["test_evidence.py::test_evidence"],
        repo_root=repo,
        require_clean=True,
    )
    assert certificate["passed"] == 1
    assert certificate["source_before"]["tracked_source_dirty"] is True
    assert certificate["tracked_source_dirty"] is False
    assert verdict is False
    assert certificate["release_eligible"] is False


def test_development_execution_can_pass_without_claiming_source_correspondence(
    scientific_git_repo,
):
    (scientific_git_repo / "helper.py").write_text("VALUE = 1\n")
    verdict, certificate = execute_nodes(
        ["test_evidence.py::test_evidence"],
        repo_root=scientific_git_repo,
    )
    assert verdict is True
    assert certificate["passed"] == 1
    assert certificate["release_eligible"] is False
    assert certificate["source_correspondence"] is False
