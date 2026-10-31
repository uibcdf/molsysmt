"""Regression tests for the agent-oriented GitHub Actions test output."""

import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
TEST_ENV = REPO / "devtools" / "conda-envs" / "test_env.yaml"
PYTEST_INI = REPO / "pytest.ini"
WORKFLOWS = (
    REPO / ".github" / "workflows" / "ci-full.yaml",
    REPO / ".github" / "workflows" / "ci-smoke.yaml",
    REPO / ".github" / "workflows" / "ci-weekly.yaml",
)
CONTROLLED_HARD_DEPENDENCIES = REPO / "devtools" / "controlled_sources.txt"


def test_ci_test_environment_pins_pytest_receptor():
    payload = yaml.safe_load(TEST_ENV.read_text(encoding="utf-8"))
    assert "pytest-receptor=1.1.0" in payload["dependencies"]
    assert "ruff=0.16.5" in payload["dependencies"]


def test_ci_installs_molsyssuite_hard_dependencies_from_exact_source_revisions():
    requirements = CONTROLLED_HARD_DEPENDENCIES.read_text(encoding="utf-8")
    for repository in (
        "smonitor",
        "depdigest",
        "pyunitwizard",
        "argdigest",
    ):
        lines = [
            line
            for line in requirements.splitlines()
            if line.startswith(f"git+https://github.com/uibcdf/{repository}@")
        ]
        assert len(lines) == 1
        revision = lines[0].rsplit("@", maxsplit=1)[1]
        assert len(revision) == 40

    environment = yaml.safe_load(TEST_ENV.read_text(encoding="utf-8"))
    names = {str(item).split("=")[0].strip() for item in environment["dependencies"]}
    assert names.isdisjoint(
        {"smonitor", "depdigest", "pyunitwizard", "argdigest", "molsysviewer"}
    )

    for workflow in WORKFLOWS:
        text = workflow.read_text(encoding="utf-8")
        assert "-r devtools/controlled_sources.txt" in text
        assert "python -m pip install --editable . --no-deps" in text
        assert "from argdigest import Domain, UnknownArgumentError" in text
        assert "PYTHONPATH" not in text
        if workflow.name == "ci-full.yaml":
            assert "inputs.molsysviewer_sha" in text
            assert "^[0-9a-f]{40}$" in text
        else:
            contract = tomllib.loads(
                (REPO / "devtools/dependency_contract.toml").read_text()
            )
            assert contract["routine_viewer_source"]["sha"] in text

    full_text = WORKFLOWS[0].read_text(encoding="utf-8")
    assert "controlled-molsysviewer-wheel" in full_text
    assert "-py3-none-any.whl" in full_text


def test_ci_validates_controlled_runtime_versions_before_pytest():
    for path in WORKFLOWS:
        workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
        guarded_jobs = 0
        for job in workflow["jobs"].values():
            steps = [step.get("run", "") for step in job.get("steps", [])]
            source_installs = [
                index
                for index, run in enumerate(steps)
                if "-r devtools/controlled_sources.txt" in run
            ]
            if not source_installs:
                continue
            guarded_jobs += 1
            checks = [
                index
                for index, run in enumerate(steps)
                if "python devtools/scripts/validate_controlled_dependencies.py" in run
            ]
            pytest_steps = [
                index
                for index, run in enumerate(steps)
                if "pytest --receptor=ci" in run
            ]
            assert len(source_installs) == len(checks) == 1
            assert pytest_steps
            assert source_installs[0] < checks[0] < min(pytest_steps)
        assert guarded_jobs


def test_ci_pytest_commands_use_the_ci_receptor():
    commands = []
    for path in WORKFLOWS:
        workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
        for job in workflow["jobs"].values():
            for step in job.get("steps", []):
                run = step.get("run", "")
                commands.extend(
                    line.strip()
                    for line in run.splitlines()
                    if re.search(r"\bpytest(?:\s|$)", line)
                    and not line.strip().startswith("#")
                )

    assert commands
    assert all(
        command.startswith("python -m pytest --receptor=ci") for command in commands
    )


def test_receptor_rerun_command_matches_ci_invocation():
    config = PYTEST_INI.read_text(encoding="utf-8")
    assert "receptor_rerun_command = python -m pytest" in config


def test_full_ci_preserves_partial_phase_evidence_after_abrupt_exit(tmp_path):
    from pytest_receptor import read_artifact

    workflow = yaml.safe_load(WORKFLOWS[0].read_text())
    steps = workflow["jobs"]["full-matrix"]["steps"]
    command = next(
        step["run"] for step in steps if step.get("name") == "Run full test suite"
    )
    (tmp_path / "pytest.ini").write_text("[pytest]\ntestpaths = .\n")
    (tmp_path / "test_abrupt.py").write_text(
        "import os\n\n"
        "def test_completed():\n    assert True\n\n"
        "def test_abrupt():\n    os._exit(17)\n"
    )
    environment = dict(os.environ)
    environment.pop("PYTEST_ADDOPTS", None)
    environment.pop("PYTEST_CURRENT_TEST", None)
    environment["PATH"] = (
        str(Path(sys.executable).parent) + os.pathsep + environment.get("PATH", "")
    )
    result = subprocess.run(
        ["bash", "-euc", command],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        timeout=45,
    )
    assert result.returncode == 17, result.stdout + result.stderr
    relative = ".pytest-receptor/events.jsonl"
    artifact = read_artifact(tmp_path / relative)
    assert not artifact.complete
    assert artifact.final is None
    phases = [record.data for record in artifact.events if record.type == "phase"]
    assert any(
        record["nodeid"] == "test_abrupt.py::test_completed"
        and record["phase"] == "call"
        and record["outcome"] == "passed"
        for record in phases
    )
    assert phases[-1]["nodeid"] == "test_abrupt.py::test_abrupt"
    assert phases[-1]["phase"] == "setup"
    assert phases[-1]["outcome"] == "passed"
    upload = next(
        step for step in steps if step.get("name") == "Upload full-suite test results"
    )
    assert upload["if"] == "always()"
    assert relative in upload["with"]["path"].splitlines()
    assert upload["with"]["include-hidden-files"] is True
