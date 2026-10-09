"""Exercise manager outcomes and fixture custody without running Conda."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("operation", ["create-conda", "create-mamba", "update"])
@pytest.mark.parametrize("manager_exit", [0, 17])
@pytest.mark.parametrize(
    "spaces", [False, True], ids=["ordinary-paths", "paths-with-spaces"]
)
def test_manager_outcome_and_caller_custody(tmp_path, operation, manager_exit, spaces):
    caller = tmp_path / ("caller workspace" if spaces else "caller")
    caller.mkdir()
    scratch = tmp_path / "owned-scratch"
    scratch.mkdir()
    bindir = tmp_path / "private-bin"
    bindir.mkdir()
    executable = bindir / ("recording manager" if spaces else "recording-manager")
    receipt = caller / "manager-receipt.json"
    executable.write_text(
        f"#!{sys.executable}\n"
        "import json, os, sys\n"
        "from pathlib import Path\n"
        "args = sys.argv[1:]\n"
        "flag = '-f' if '-f' in args else '--file'\n"
        "spec = Path(args[args.index(flag) + 1]).resolve()\n"
        "Path(os.environ['CONTROL_RECEIPT']).write_text(json.dumps({\n"
        "    'argv': args, 'cwd': str(Path.cwd()), 'spec': str(spec),\n"
        "    'manifest': spec.read_text(), 'spec_existed_during_child': spec.exists()}))\n"
        "raise SystemExit(int(os.environ['CONTROL_EXIT']))\n",
        encoding="utf-8",
    )
    executable.chmod(0o700)
    spec = caller / ("caller input.yaml" if spaces else "caller-input.yaml")
    original = "channels: [conda-forge]\ndependencies: [python >=3.11, pytest]\n"
    spec.write_text(original, encoding="utf-8")
    prefix = caller / "caller-environment"
    prefix.mkdir()
    sentinel = prefix / "caller-owned"
    sentinel.write_text("keep", encoding="utf-8")
    env = dict(os.environ)
    env.pop("MAMBA_EXE", None)
    env.update(
        CONDA_EXE=str(executable),
        PATH=str(bindir),
        TMPDIR=str(scratch),
        TEMP=str(scratch),
        TMP=str(scratch),
        CONTROL_RECEIPT=str(receipt),
        CONTROL_EXIT=str(manager_exit),
    )
    name = "caller environment" if spaces else "caller_environment"
    if operation.startswith("create"):
        if operation == "create-mamba":
            env["MAMBA_EXE"] = str(executable)
        command = [
            sys.executable,
            str(ROOT / "devtools/conda-envs/create_conda_env.py"),
            "-n",
            name,
            "-p",
            "3.14",
            str(spec),
        ]
        expected = ["env", "create", "-n", name, "-f", "temp_script.yaml"]
    else:
        command = [
            sys.executable,
            str(ROOT / "devtools/conda-envs/update_conda_env.py"),
            str(spec),
        ]
        expected = ["env", "update", "--file", str(spec), "--prune"]
    result = subprocess.run(
        command, cwd=caller, env=env, capture_output=True, text=True, timeout=20
    )
    assert (result.returncode == 0) == (manager_exit == 0), (
        result.stdout + result.stderr
    )
    assert receipt.exists(), result.stdout + result.stderr
    observed = json.loads(receipt.read_text())
    assert observed["argv"] == expected
    assert observed["spec_existed_during_child"]
    assert spec.read_text(encoding="utf-8") == original
    assert sentinel.read_text(encoding="utf-8") == "keep"
    assert not list(scratch.iterdir())
    if operation.startswith("create"):
        assert not Path(observed["cwd"]).exists()
        assert not Path(observed["spec"]).exists()
        assert yaml.safe_load(observed["manifest"])["dependencies"] == [
            "python 3.14*",
            "pytest",
        ]
    else:
        assert observed["cwd"] == str(caller)
        assert observed["spec"] == str(spec)
