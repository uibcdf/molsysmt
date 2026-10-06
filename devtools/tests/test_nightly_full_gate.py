"""The nightly CI debt survives skipped commits and failed full matrices."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from urllib.error import URLError

import pytest
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
                    "conclusion": "failure" if run_id == 3 else "success",
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


def test_publisher_failure_does_not_repeat_an_already_successful_full_matrix(
    monkeypatch,
):
    def api(path, _token):
        if "/runs?" in path:
            return (
                {
                    "workflow_runs": [
                        {
                            "id": 1,
                            "event": "schedule",
                            "head_sha": "matrix",
                            "conclusion": "failure",
                        }
                    ]
                }
                if "ci-weekly.yaml" in path
                else {"workflow_runs": []}
            )
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
                for version in gate.FULL_VERSIONS
            ]
        }

    monkeypatch.setattr(gate, "api_json", api)
    monkeypatch.setattr(gate, "is_ancestor", lambda *_: True)
    assert gate.last_full_success("uibcdf/molsysmt", "head", "token") == "matrix"


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
    assert (
        "steps.suite.outputs.exit_code == '0' || steps.suite.outputs.exit_code == '1'"
        in retain["if"]
    )
    assert "!cancelled()" in retain["if"]
    publisher = workflow["jobs"]["coverage-upload"]
    assert publisher["needs"] == "full"
    assert "always()" in publisher["if"] and "!cancelled()" in publisher["if"]
    assert "github.ref == 'refs/heads/main'" in publisher["if"]
    assert "needs.full.result == 'failure'" in publisher["if"]
    assert publisher["with"]["source_run_id"] == "${{ github.run_id }}"
    assert publisher["uses"] == "./.github/workflows/ci-coverage-upload.yaml"
    assert not any("codecov/codecov-action" in s.get("uses", "") for s in steps)
    assert "id-token" not in workflow["permissions"]
    assert publisher["permissions"]["id-token"] == "write"


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


@pytest.mark.parametrize("missing", ["3.11", "3.12", "3.13", "3.14"])
@pytest.mark.parametrize("workflow", ["ci-weekly.yaml", "ci-full.yaml"])
def test_each_accepted_minor_must_execute_to_clear_backlog(
    monkeypatch, missing, workflow
):
    prefix, step = gate.FULL_WORKFLOWS[workflow]
    jobs = [
        {
            "name": f"{prefix} — ubuntu-latest, Python {minor}",
            "conclusion": "success",
            "steps": [{"name": step, "conclusion": "success"}],
        }
        for minor in ["3.11", "3.12", "3.13", "3.14"]
    ]
    monkeypatch.setattr(gate, "api_json", lambda *_: {"jobs": jobs})
    assert gate.full_matrix_passed("uibcdf/molsysmt", 1, "token", workflow)
    jobs[:] = [job for job in jobs if not job["name"].endswith(missing)]
    assert not gate.full_matrix_passed("uibcdf/molsysmt", 1, "token", workflow)


def test_routine_and_full_routes_cover_the_accepted_python_policy():
    workflows = REPO / ".github/workflows"
    for filename, job in [("ci-smoke.yaml", "smoke"), ("benchmarks.yml", "benchmark")]:
        workflow = yaml.safe_load((workflows / filename).read_text())
        assert workflow["jobs"][job]["strategy"]["matrix"]["cfg"] == [
            {"os": "ubuntu-latest", "python-version": "3.14"}
        ]
    candidate = yaml.safe_load((workflows / "ci-full.yaml").read_text())
    cells = candidate["jobs"]["full-matrix"]["strategy"]["matrix"]["cfg"]
    assert {(cell["os"], cell["python-version"]) for cell in cells} == {
        (platform, minor)
        for platform in ["ubuntu-latest", "macos-15"]
        for minor in ["3.11", "3.12", "3.13", "3.14"]
    }
    assert len(cells) == 8


def test_weekly_routes_have_mac_arm64_and_distinct_retained_artifacts():
    workflow = yaml.safe_load((REPO / ".github/workflows/ci-weekly.yaml").read_text())
    full = workflow["jobs"]["full"]
    expression = full["strategy"]["matrix"]["cfg"]
    manual, default = [
        json.loads(value) for value in re.findall(r"'(\[.*?\])'", expression)
    ]
    assert manual == [{"os": "ubuntu-latest", "python-version": "3.13"}]
    assert {(cell["os"], cell["python-version"]) for cell in default} == {
        ("ubuntu-latest", minor) for minor in ["3.11", "3.12", "3.13", "3.14"]
    } | {("macos-15", "3.14")}
    for step in full["steps"]:
        if step.get("uses", "").startswith("actions/upload-artifact@"):
            template = step["with"]["name"]
            names = [
                template.replace(
                    "${{ matrix.cfg.python-version }}", cell["python-version"]
                ).replace(
                    "${{ matrix.cfg.os == 'macos-15' && '-macos-arm64' || '' }}",
                    "-macos-arm64" if cell["os"] == "macos-15" else "",
                )
                for cell in default
            ]
            assert not any("${{" in name for name in names)
            assert len(names) == len(set(names))
            if step["name"] == "Retain coverage and test results":
                assert "full-suite-coverage-py3.13" in names
