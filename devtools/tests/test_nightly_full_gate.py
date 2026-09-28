"""The nightly CI debt survives skipped commits and failed full matrices."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from urllib.error import URLError

import yaml

from devtools.scripts import nightly_full_gate as gate

REPO = Path(__file__).resolve().parents[2]


def _git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def test_skip_markers_remain_due_after_the_last_green_commit(tmp_path, monkeypatch):
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "config", "user.name", "CI test")
    _git(tmp_path, "config", "user.email", "ci@example.invalid")
    _git(tmp_path, "commit", "--allow-empty", "-qm", "green full suite")
    anchor = _git(tmp_path, "rev-parse", "HEAD")
    _git(tmp_path, "commit", "--allow-empty", "-qm", "fast change [skip ci]")
    skipped = _git(tmp_path, "rev-parse", "HEAD")
    _git(tmp_path, "commit", "--allow-empty", "-qm", "ordinary change")
    head = _git(tmp_path, "rev-parse", "HEAD")
    monkeypatch.chdir(tmp_path)

    assert gate.skipped_commits_after(anchor, head) == [skipped]
    assert gate.skipped_commits_after(head, head) == []
    assert gate.SKIP_MARKER.search("message\n\nskip-checks: true")


def test_only_executed_successful_full_matrix_clears_backlog(monkeypatch):
    runs = [
        {"id": 2, "event": "schedule", "head_sha": "newer"},
        {"id": 1, "event": "workflow_dispatch", "head_sha": "green"},
    ]

    def fake_api(path, _token):
        if "/runs?" in path:
            return {"workflow_runs": runs}
        run_id = 2 if "/runs/2/" in path else 1
        return {
            "jobs": [
                {
                    "name": f"Full test — ubuntu-latest, Python {version}",
                    "conclusion": "success",
                    "steps": [
                        {
                            "name": "Run full test suite with coverage",
                            "conclusion": "skipped" if run_id == 2 else "success",
                        }
                    ],
                }
                for version in gate.FULL_VERSIONS
            ]
        }

    monkeypatch.setattr(gate, "api_json", fake_api)
    monkeypatch.setattr(gate, "is_ancestor", lambda _commit, _head: True)
    assert gate.last_full_success("uibcdf/molsysmt", "head", "token") == "green"


def test_api_uncertainty_runs_full_suite(tmp_path, monkeypatch):
    output = tmp_path / "github-output"
    monkeypatch.setenv("GITHUB_REPOSITORY", "uibcdf/molsysmt")
    monkeypatch.setenv("GITHUB_SHA", "head")
    monkeypatch.setenv("GITHUB_TOKEN", "token")
    monkeypatch.setenv("GITHUB_OUTPUT", str(output))

    def offline(*_):
        raise URLError("offline")

    monkeypatch.setattr(gate, "last_full_success", offline)
    assert gate.main() == 0
    assert "run_full=true" in output.read_text(encoding="utf-8")


def test_tests_badge_names_an_existing_workflow():
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    assert "actions/workflows/ci-smoke.yaml/badge.svg" in readme
    assert (REPO / ".github/workflows/ci-smoke.yaml").is_file()


def test_nightly_recovery_and_pr_full_suite_are_connected():
    workflows = REPO / ".github/workflows"
    weekly = yaml.load(
        (workflows / "ci-weekly.yaml").read_text(encoding="utf-8"),
        Loader=yaml.BaseLoader,
    )
    assert any(
        item.get("timezone") == "America/Mexico_City"
        for item in weekly["on"]["schedule"]
    )
    decision = weekly["jobs"]["nightly-decision"]
    assert any(
        "nightly_full_gate.py" in step.get("run", "") for step in decision["steps"]
    )
    full = weekly["jobs"]["full"]
    assert full["needs"] == "nightly-decision"
    assert "run_full" in full["if"]

    candidate = yaml.load(
        (workflows / "ci-full.yaml").read_text(encoding="utf-8"),
        Loader=yaml.BaseLoader,
    )
    assert "pull_request" in candidate["on"]
    assert set(candidate["jobs"]["pr-gate"]["needs"]) == {
        "controlled-molsysviewer",
        "full-matrix",
    }


def test_push_smoke_runs_only_the_bounded_local_tier():
    smoke = yaml.load(
        (REPO / ".github/workflows/ci-smoke.yaml").read_text(encoding="utf-8"),
        Loader=yaml.BaseLoader,
    )
    run = next(
        step["run"]
        for step in smoke["jobs"]["smoke"]["steps"]
        if step.get("name") == "Run test suite"
    )
    paths = re.findall(r"tests/[A-Za-z0-9_./]+\.py", run)
    assert "python -m pytest --receptor=ci" in run
    assert len(paths) == 4
    local_tier = (REPO / "devtools/tests/run_tiers.sh").read_text(encoding="utf-8")
    assert all(path in local_tier for path in paths)
