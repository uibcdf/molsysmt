"""Ensure every bound-addon regression belongs to the hosted pytest command."""

import re
import shlex
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def test_all_addon_test_modules_are_arguments_of_one_pytest_invocation():
    workflow = yaml.safe_load((ROOT / ".github/workflows/ci-smoke.yaml").read_text())
    runs = [s.get("run", "") for s in workflow["jobs"]["smoke"]["steps"]]
    scripts = [run for run in runs if "tests/molsysviewer_molsysmt/" in run]
    assert len(scripts) == 1
    script = scripts[0]
    commands = [
        shlex.split(line, comments=True)
        for line in script.replace("\\\n", " ").splitlines()
    ]
    pytest = [argv for argv in commands if argv[:3] == ["python", "-m", "pytest"]]
    assert len(pytest) == 1
    expected = {
        p.relative_to(ROOT).as_posix()
        for p in (ROOT / "tests/molsysviewer_molsysmt").glob("test_*.py")
    }
    selected = {a for a in pytest[0] if a.startswith("tests/molsysviewer_molsysmt/")}
    declared = set(re.findall(r"tests/molsysviewer_molsysmt/[\w]+\.py", script))
    assert selected == declared == expected
    assert not any(argv and argv[0].startswith("tests/") for argv in commands)
