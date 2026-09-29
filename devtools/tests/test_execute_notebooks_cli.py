"""Exercise CLI exit status with a controlled notebook execution process."""

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parents[2] / "docs" / "execute_notebooks.py"
_CONTROLLED_KERNEL = """
import runpy
import subprocess
import sys
from pathlib import Path

def notebook_process(arguments, **kwargs):
    assert arguments[:2] == ["jupyter", "nbconvert"]
    failed = Path(arguments[-1]).name == "fail.ipynb"
    return subprocess.CompletedProcess(arguments, int(failed), "", "controlled kernel failure" if failed else "")

subprocess.run = notebook_process
script = sys.argv.pop(1)
sys.argv[0] = script
runpy.run_path(script, run_name="__main__")
"""


def _run_cli(tmp_path, names):
    script = tmp_path / "execute_notebooks.py"
    shutil.copyfile(_SCRIPT, script)
    for name in names:
        if name != "missing.ipynb":
            (tmp_path / name).write_text(json.dumps({
                "cells": [{"cell_type": "code", "source": ["pass"],
                           "outputs": [], "metadata": {}}],
                "metadata": {}, "nbformat": 4, "nbformat_minor": 0,
            }))
    return subprocess.run(
        [sys.executable, "-c", _CONTROLLED_KERNEL, str(script), "-q", "-f", *names],
        cwd=tmp_path, capture_output=True, text=True, timeout=30,
    )


@pytest.mark.parametrize("names", [
    ["fail.ipynb"], ["ok.ipynb", "fail.ipynb"], ["fail.ipynb", "ok.ipynb"],
])
def test_cli_exits_nonzero_when_any_notebook_fails(tmp_path, names):
    result = _run_cli(tmp_path, names)
    assert "1 notebook(s) failed" in result.stdout
    assert result.returncode != 0


def test_cli_success_returns_zero(tmp_path):
    result = _run_cli(tmp_path, ["ok.ipynb"])
    assert result.returncode == 0
    assert "1 executed" in result.stdout


def test_cli_missing_input_returns_nonzero(tmp_path):
    result = _run_cli(tmp_path, ["missing.ipynb"])
    assert "File not found" in result.stdout
    assert result.returncode != 0
