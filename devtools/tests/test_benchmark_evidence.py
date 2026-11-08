"""Exercise evidence publication without running molecular benchmarks."""

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def runner(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location(
        "isolated_matrix_runner", ROOT / "benchmarks/competitors/run_matrix.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "repo_root", str(tmp_path))
    original = tmp_path / "solvated_villin.pdb"
    original.write_bytes(b"CALLER_OWNED_REFERENCE")
    baseline = tmp_path / "benchmarks/baselines/competitor_matrix_session.json"
    baseline.parent.mkdir(parents=True)
    baseline.write_bytes(b"ORIGINAL_BASELINE")
    seen = []

    def prepare(path):
        seen.append(Path(path))
        Path(path).write_text("TEST_REFERENCE")

    monkeypatch.setattr(module, "_prepare_reference", prepare)
    for index, name in enumerate(
        [
            "run_loading_benchmarks",
            "run_selection_benchmarks",
            "run_geometry_benchmarks",
        ]
    ):

        def phase(path, results, index=index):
            assert Path(path).read_text() == "TEST_REFERENCE"
            results.append(
                {
                    "name": f"fixture_{index}",
                    "median_seconds": float(index + 1),
                    "peak_rss_mb": 0.0,
                }
            )

        monkeypatch.setattr(module, name, phase)
    return module, seen, original, baseline


def test_explicit_session_does_not_renew_baseline_or_touch_a_caller_reference(
    runner, tmp_path
):
    module, seen, original, baseline = runner
    target = tmp_path / "evidence/current.json"
    module.main(["--output", str(target)])
    assert baseline.read_bytes() == b"ORIGINAL_BASELINE"
    assert original.read_bytes() == b"CALLER_OWNED_REFERENCE"
    assert len(seen) == 1 and not seen[0].exists()
    result = json.loads(target.read_text())
    assert [v["median_seconds"] for v in result["results"].values()] == [1.0, 2.0, 3.0]
    assert result["session_name"] == "competitive-performance-matrix"
    assert result["environment"]["python"]


def test_relative_output_without_a_parent_directory_works(
    runner, tmp_path, monkeypatch
):
    module, seen, original, baseline = runner
    monkeypatch.chdir(tmp_path)
    module.main(["--output", "current.json"])
    assert (tmp_path / "current.json").is_file()
    assert baseline.read_bytes() == b"ORIGINAL_BASELINE"
    assert original.read_bytes() == b"CALLER_OWNED_REFERENCE"


@pytest.mark.parametrize(
    "failed_phase",
    [
        "_prepare_reference",
        "run_loading_benchmarks",
        "run_selection_benchmarks",
        "run_geometry_benchmarks",
    ],
)
def test_failed_campaign_cleans_only_its_reference_and_publishes_no_session(
    runner, tmp_path, monkeypatch, failed_phase
):
    module, seen, original, baseline = runner

    def fail(*args):
        if failed_phase == "_prepare_reference":
            seen.append(Path(args[0]))
            Path(args[0]).write_text("PARTIAL_TEST_REFERENCE")
        raise RuntimeError("controlled campaign failure")

    monkeypatch.setattr(module, failed_phase, fail)
    target = tmp_path / "failed.json"
    with pytest.raises(RuntimeError, match="controlled campaign failure"):
        module.main(["--output", str(target)])
    assert seen and all(not p.exists() for p in seen)
    assert not target.exists()
    assert original.read_bytes() == b"CALLER_OWNED_REFERENCE"
    assert baseline.read_bytes() == b"ORIGINAL_BASELINE"


def test_directory_output_is_rejected_before_any_campaign(runner, tmp_path):
    module, seen, original, baseline = runner
    with pytest.raises(SystemExit) as err:
        module.main(["--output", str(tmp_path)])
    assert err.value.code == 2 and seen == []
    assert baseline.read_bytes() == b"ORIGINAL_BASELINE"


@pytest.mark.parametrize("value,expected", [(0.9, 0), (1.2, 1)])
def test_actual_workflow_pipeline_preserves_comparison_exit_and_raw_inputs(
    tmp_path, value, expected
):
    workflow = yaml.safe_load((ROOT / ".github/workflows/benchmarks.yml").read_text())
    steps = workflow["jobs"]["benchmark"]["steps"]
    script = next(
        s["run"] for s in steps if s.get("name") == "Audit Performance Regressions"
    )
    comparer = tmp_path / "benchmarks/compare_runs.py"
    comparer.parent.mkdir()
    shutil.copyfile(ROOT / "benchmarks/compare_runs.py", comparer)
    evidence = tmp_path / ".pytest_cache/benchmark-evidence"
    evidence.mkdir(parents=True)
    reference = evidence / "reference_session.json"
    current = evidence / "current_session.json"
    reference.write_text(json.dumps({"results": {"product": {"median_seconds": 1.0}}}))
    current.write_text(json.dumps({"results": {"product": {"median_seconds": value}}}))
    before = [hashlib.sha256(p.read_bytes()).hexdigest() for p in [reference, current]]
    result = subprocess.run(
        ["bash", "-c", script],
        cwd=tmp_path,
        env={
            **os.environ,
            "PATH": str(Path(sys.executable).parent)
            + os.pathsep
            + os.environ.get("PATH", ""),
            "BENCHMARK_EVIDENCE_DIR": str(evidence),
        },
        capture_output=True,
        text=True,
    )
    assert result.returncode == expected, result.stdout + result.stderr
    assert (evidence / "comparison.log").read_text() == result.stdout
    assert before == [
        hashlib.sha256(p.read_bytes()).hexdigest() for p in [reference, current]
    ]
    upload = steps[-1]
    assert upload["if"] == "always() && steps.reference.outcome == 'success'"
    assert upload["with"]["path"] == ".pytest_cache/benchmark-evidence/"
    assert upload["with"]["include-hidden-files"] is True
    assert upload["with"]["if-no-files-found"] == "error"


def test_actual_measurement_pipeline_retains_failure_status_and_log(tmp_path):
    workflow = yaml.safe_load((ROOT / ".github/workflows/benchmarks.yml").read_text())
    script = next(
        s["run"]
        for s in workflow["jobs"]["benchmark"]["steps"]
        if s.get("name") == "Run Current Benchmarks"
    )
    producer = tmp_path / "benchmarks/competitors/run_matrix.py"
    producer.parent.mkdir(parents=True)
    producer.write_text(
        "import os, sys\nassert os.environ['SMONITOR_PROFILE']=='qa'\nprint('controlled measurement failure', flush=True)\nsys.exit(7)\n"
    )
    evidence = tmp_path / ".pytest_cache/benchmark-evidence"
    evidence.mkdir(parents=True)
    result = subprocess.run(
        ["bash", "-c", script],
        cwd=tmp_path,
        env={
            **os.environ,
            "PATH": str(Path(sys.executable).parent)
            + os.pathsep
            + os.environ.get("PATH", ""),
            "BENCHMARK_EVIDENCE_DIR": str(evidence),
        },
        capture_output=True,
        text=True,
    )
    assert result.returncode == 7
    assert (
        (evidence / "current.log").read_text()
        == result.stdout
        == "controlled measurement failure\n"
    )
    assert not (evidence / "current_session.json").exists()


def test_manual_default_retains_the_existing_baseline_destination(runner):
    module, seen, original, baseline = runner
    module.main([])
    assert (
        json.loads(baseline.read_text())["session_name"]
        == "competitive-performance-matrix"
    )
    assert original.read_bytes() == b"CALLER_OWNED_REFERENCE"
    assert seen and all(not path.exists() for path in seen)
