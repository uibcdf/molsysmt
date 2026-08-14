"""Regression tests for the agent-oriented GitHub Actions test output."""

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
CONTROLLED_HARD_DEPENDENCIES = (
    REPO / "devtools" / "requirements" / "controlled_hard_dependencies.txt"
)


def test_ci_test_environment_pins_pytest_receptor():
    payload = yaml.safe_load(TEST_ENV.read_text(encoding="utf-8"))
    assert "pytest-receptor=0.6.0" in payload["dependencies"]
    assert "ruff" in payload["dependencies"]


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
        assert "-r devtools/requirements/controlled_hard_dependencies.txt" in text
        assert "python -m pip install --editable . --no-deps" in text
        assert "from argdigest import Domain, UnknownArgumentError" in text
        assert "PYTHONPATH" not in text
        assert "7a1522662e30575caf580a9447e3e6d80b628e07" in text

    full_text = WORKFLOWS[0].read_text(encoding="utf-8")
    assert "controlled-molsysviewer-wheel" in full_text
    assert "-py3-none-any.whl" in full_text


def test_ci_pytest_commands_use_the_ci_receptor():
    commands = []
    for path in WORKFLOWS:
        workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
        for job in workflow["jobs"].values():
            for step in job["steps"]:
                run = step.get("run", "")
                commands.extend(
                    line.strip()
                    for line in run.splitlines()
                    if "pytest" in line and not line.strip().startswith("#")
                )

    assert commands
    assert all(
        command.startswith("python -m pytest --receptor=ci")
        for command in commands
    )


def test_receptor_rerun_command_matches_ci_invocation():
    config = PYTEST_INI.read_text(encoding="utf-8")
    assert "receptor_rerun_command = python -m pytest" in config
