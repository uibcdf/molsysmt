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
    weekly_runs = [
        {"id": 3, "event": "schedule", "head_sha": "failed", "conclusion": "failure"},
        {"id": 2, "event": "schedule", "head_sha": "newer", "conclusion": "success"},
        {
            "id": 1,
            "event": "workflow_dispatch",
            "head_sha": "green",
            "conclusion": "success",
        },
    ]
    candidate_runs = [
        {
            "id": 4,
            "event": "workflow_dispatch",
            "head_sha": "candidate",
            "conclusion": "success",
        }
    ]

    def fake_api(path, _token):
        if "/runs?" in path:
            assert "status=success" not in path
            return {
                "workflow_runs": candidate_runs
                if "/workflows/ci-full.yaml/" in path
                else weekly_runs
            }
        run_id = int(path.split("/runs/")[1].split("/")[0])
        prefix, test_step = (
            ("Full matrix", "Run full test suite")
            if run_id == 4
            else ("Full test", "Run full test suite with coverage")
        )
        return {
            "jobs": [
                {
                    "name": f"{prefix} — ubuntu-latest, Python {version}",
                    "conclusion": "success",
                    "steps": [
                        {
                            "name": test_step,
                            "conclusion": "skipped" if run_id == 2 else "success",
                        }
                    ],
                }
                for version in gate.FULL_VERSIONS
            ]
        }

    monkeypatch.setattr(gate, "api_json", fake_api)
    order = {"green": 0, "candidate": 1, "newer": 2, "failed": 3, "head": 4}
    monkeypatch.setattr(
        gate, "is_ancestor", lambda older, newer: order[older] <= order[newer]
    )
    assert gate.last_full_success("uibcdf/molsysmt", "head", "token") == "candidate"


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


def test_probe_output_binds_large_backlogs(tmp_path, monkeypatch, capsys):
    output = tmp_path / "github-output"
    monkeypatch.setenv("GITHUB_REPOSITORY", "uibcdf/molsysmt")
    monkeypatch.setenv("GITHUB_SHA", "head")
    monkeypatch.setenv("GITHUB_TOKEN", "token")
    monkeypatch.setenv("GITHUB_OUTPUT", str(output))
    monkeypatch.setattr(gate, "last_full_success", lambda *_: "anchor")
    monkeypatch.setattr(
        gate, "skipped_commits_after", lambda *_: [f"commit-{i}" for i in range(20)]
    )

    assert gate.main() == 0
    printed = capsys.readouterr().out
    assert "Skipped commits pending: 20" in printed
    assert "commit-4" in printed
    assert "commit-5" not in printed
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
    assert (
        weekly["on"]["workflow_dispatch"]["inputs"]["probe_backlog"]["default"]
        == "false"
    )
    assert "inputs.probe_backlog == true" in decision["if"]
    full = weekly["jobs"]["full"]
    assert full["needs"] == "nightly-decision"
    assert "run_full" in full["if"]
    assert "inputs.probe_backlog != true" in full["if"]

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


def test_single_python_coverage_cannot_clear_the_full_matrix_backlog(monkeypatch):
    def jobs(versions):
        return {
            "jobs": [
                {
                    "name": f"Full test — ubuntu-latest, Python {version}",
                    "conclusion": "success",
                    "steps": [
                        {
                            "name": "Run full test suite with coverage",
                            "conclusion": "success",
                        }
                    ],
                }
                for version in versions
            ]
        }

    monkeypatch.setattr(gate, "api_json", lambda *_: jobs(["3.13"]))
    assert not gate.full_matrix_passed("uibcdf/molsysmt", 1, "token", "ci-weekly.yaml")
    monkeypatch.setattr(gate, "api_json", lambda *_: jobs(gate.FULL_VERSIONS))
    assert gate.full_matrix_passed("uibcdf/molsysmt", 1, "token", "ci-weekly.yaml")


def test_coverage_retention_preserves_failures_and_rejects_aborted_suites(tmp_path):
    import os

    workflow = yaml.load(
        (REPO / ".github/workflows/ci-weekly.yaml").read_text(),
        Loader=yaml.BaseLoader,
    )
    steps = workflow["jobs"]["full"]["steps"]
    suite = next(step for step in steps if step.get("id") == "suite")
    assert "continue-on-error" not in suite
    command = suite["run"]
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    executable = bin_dir / "python"
    for status in (0, 1, 2):
        executable.write_text(f"#!/bin/sh\nexit {status}\n")
        executable.chmod(0o755)
        output = tmp_path / f"output-{status}"
        env = dict(
            os.environ,
            PATH=f"{bin_dir}:{os.environ['PATH']}",
            GITHUB_OUTPUT=str(output),
        )
        result = subprocess.run(
            ["bash", "-c", command], cwd=tmp_path, env=env, check=False
        )
        assert result.returncode == status
        assert output.read_text().strip() == f"exit_code={status}"
    retain = next(
        step for step in steps if step.get("name") == "Retain coverage and test results"
    )
    upload = next(
        step for step in steps if step.get("name") == "Upload coverage to Codecov"
    )
    for step in (retain, upload):
        assert (
            "steps.suite.outputs.exit_code == '0' || steps.suite.outputs.exit_code == '1'"
            in step["if"]
        )
        assert "!cancelled()" in step["if"]
    assert "github.ref == 'refs/heads/main'" in upload["if"]
    assert upload["with"]["fail_ci_if_error"] == "true"
    assert upload["with"]["disable_search"] == "true"


def test_only_an_explicit_manual_request_selects_the_single_coverage_lane():
    workflow = yaml.load(
        (REPO / ".github/workflows/ci-weekly.yaml").read_text(),
        Loader=yaml.BaseLoader,
    )
    option = workflow["on"]["workflow_dispatch"]["inputs"]["python_313_only"]
    assert option["type"] == "boolean" and option["default"] == "false"
    matrix = workflow["jobs"]["full"]["strategy"]["matrix"]["cfg"]
    assert (
        "github.event_name == 'workflow_dispatch' && inputs.python_313_only == true"
        in matrix
    )
    assert 'python-version":"3.11' in matrix and 'python-version":"3.12' in matrix
    assert matrix.count('python-version":"3.13') == 2
