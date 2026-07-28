"""Regression tests for the agent-oriented GitHub Actions test output."""

from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parents[2]
TEST_ENV = REPO / "devtools" / "conda-envs" / "test_env.yaml"
PYTEST_INI = REPO / "pytest.ini"
WORKFLOWS = (
    REPO / ".github" / "workflows" / "ci-full.yaml",
    REPO / ".github" / "workflows" / "ci-weekly.yaml",
)


def test_ci_test_environment_pins_pytest_receptor():
    payload = yaml.safe_load(TEST_ENV.read_text(encoding="utf-8"))
    assert "pytest-receptor=0.6.0" in payload["dependencies"]


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
