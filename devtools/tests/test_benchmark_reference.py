"""Protect the benchmark's compiled source route and real H5 preparation."""

import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def _prepare_in_fresh_process(tmp_path, *, without_rust=False):
    program = ""
    if without_rust:
        program += """
import importlib.util
original_find_spec = importlib.util.find_spec
def without_backend(name, *args, **kwargs):
    if name == 'molsysmt._rust':
        return None
    return original_find_spec(name, *args, **kwargs)
importlib.util.find_spec = without_backend
"""
    program += """
import runpy
import sys
namespace = runpy.run_path(sys.argv[1])
namespace['_prepare_reference'](sys.argv[2])
"""
    return subprocess.run(
        [
            sys.executable,
            "-c",
            program,
            str(ROOT / "benchmarks/competitors/run_matrix.py"),
            str(tmp_path / "reference.pdb"),
        ],
        cwd=tmp_path,
        env=dict(os.environ, SMONITOR_PROFILE="qa", OMP_NUM_THREADS="1"),
        text=True,
        capture_output=True,
        timeout=180,
    )


def test_real_h5_reference_converts_in_a_fresh_source_process(tmp_path):
    result = _prepare_in_fresh_process(tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    runtime = json.loads(
        next(
            line.removeprefix("BENCHMARK_RUNTIME ")
            for line in result.stdout.splitlines()
            if line.startswith("BENCHMARK_RUNTIME ")
        )
    )
    assert runtime["rust"] and runtime["input_exists"]
    assert Path(runtime["molsysmt"]).parent == ROOT / "molsysmt"
    assert runtime["python"] == sys.executable
    assert runtime["input_bytes"] == 1268562
    assessment = json.loads(
        next(
            line.removeprefix("BENCHMARK_REFERENCE ")
            for line in result.stdout.splitlines()
            if line.startswith("BENCHMARK_REFERENCE ")
        )
    )
    assert assessment == {"forms": ["file:h5"], "reason": None, "valid": True}

    import mdtraj
    import numpy as np

    reference = mdtraj.load_hdf5(runtime["input"])
    actual = mdtraj.load_pdb(str(tmp_path / "reference.pdb"))
    assert actual.xyz.shape == reference.xyz.shape == (20, 4369, 3)
    np.testing.assert_allclose(actual.xyz, reference.xyz, atol=0.000051, rtol=0)
    assert not (
        tmp_path / "benchmarks/baselines/competitor_matrix_session.json"
    ).exists()


def test_missing_backend_stops_before_reference_conversion(tmp_path):
    result = _prepare_in_fresh_process(tmp_path, without_rust=True)
    assert result.returncode != 0
    assert "cannot find molsysmt._rust" in result.stderr
    assert '"rust": null' in result.stdout
    assert not (tmp_path / "reference.pdb").exists()


def test_ci_installs_the_compiled_checkout_before_preparation_and_timing():
    workflow = yaml.safe_load((ROOT / ".github/workflows/benchmarks.yml").read_text())
    steps = workflow["jobs"]["benchmark"]["steps"]
    commands = [
        shlex.split(line)
        for step in steps
        for line in step.get("run", "").replace("\\\n", " ").splitlines()
        if line.strip().startswith("python -m pip install")
    ]
    local = [command for command in commands if "." in command]
    assert len(local) == 1
    assert "--editable" in local[0] or "-e" in local[0]
    assert "--no-deps" in local[0]
    guard = next(
        i
        for i, step in enumerate(steps)
        if "devtools/tests/test_benchmark_reference.py" in step.get("run", "")
    )
    timing = next(
        i
        for i, step in enumerate(steps)
        if "python benchmarks/competitors/run_matrix.py" in step.get("run", "")
    )
    install = next(
        i
        for i, step in enumerate(steps)
        if any(
            shlex.split(line) == local[0]
            for line in step.get("run", "").replace("\\\n", " ").splitlines()
            if line.strip().startswith("python -m pip install")
        )
    )
    assert install < guard < timing
    audit = next(
        step for step in steps if step.get("name") == "Audit Performance Regressions"
    )
    assert "--threshold 0.15" in audit["run"]
