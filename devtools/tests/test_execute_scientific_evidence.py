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


def test_release_certificate_requires_a_clean_git_commit(tmp_path):
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
