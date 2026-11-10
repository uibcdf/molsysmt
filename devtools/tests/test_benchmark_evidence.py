"""Exercise evidence publication without running molecular benchmarks."""

import hashlib
import importlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from devtools.tests.benchmark_fixtures import session

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


@pytest.mark.parametrize("value,expected", [(0.9, 0), (1.2, 0)])
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
    for name in ["compare_runs.py", "comparability.py", "telemetry.py"]:
        shutil.copyfile(ROOT / "benchmarks" / name, comparer.parent / name)
    evidence = tmp_path / ".pytest_cache/benchmark-evidence"
    evidence.mkdir(parents=True)
    reference = evidence / "reference_session.json"
    current = evidence / "current_session.json"
    reference.write_text(json.dumps(session()))
    current.write_text(json.dumps(session(value)))
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


def test_performance_workflow_is_advisory_without_hiding_evidence_failures():
    workflow = yaml.safe_load((ROOT / ".github/workflows/benchmarks.yml").read_text())
    job = workflow["jobs"]["benchmark"]
    assert job["continue-on-error"] is True
    assert "advisory" in workflow["name"].lower()
    # Native failures remain visible and artifacts are retained; no `|| true`.
    for name in ["Run Current Benchmarks", "Audit Performance Regressions"]:
        script = next(step["run"] for step in job["steps"] if step.get("name") == name)
        assert "set -euo pipefail" in script
        assert "|| true" not in script


def test_owned_reference_canonicalization_preserves_every_scientific_record(tmp_path):
    from benchmarks.competitors.run_matrix import _canonicalize_owned_reference

    payload = (
        b"REMARK 350 BIOMOLECULE: 1\n"
        b"CRYST1   10.000   10.000   10.000  90.00  90.00  90.00 P 1\n"
        b"ATOM      1  CA  ALA A   1       0.500   0.500   0.500\n"
        b"CONECT    1    2\nEND\n"
    )
    records = []
    for number, clock in enumerate(
        [b"01-JAN-2020 at 01:02:03", b"02-JAN-2020 at 12:34:56"]
    ):
        path = tmp_path / f"owned-{number}.pdb"
        raw = (
            b"HEADER    MOLECULAR SYSTEM                         DIFFERENT DATE\n"
            + b"REMARK   1 Created by MolSysMT version test on "
            + clock
            + b"\n"
            + payload
        )
        path.write_bytes(raw)
        record = _canonicalize_owned_reference(path)
        prepared = path.read_bytes()
        assert (
            prepared.splitlines(keepends=True)[2:] == raw.splitlines(keepends=True)[2:]
        )
        assert prepared.endswith(payload)
        restored = prepared.splitlines(keepends=True)
        for index, original in record["original_records"].items():
            restored[int(index)] = original.encode("ascii")
        assert b"".join(restored) == raw
        assert record["raw_pdb_sha256"] == hashlib.sha256(raw).hexdigest()
        assert record["prepared_pdb_sha256"] == hashlib.sha256(prepared).hexdigest()
        records.append(record)
    assert records[0]["prepared_pdb_sha256"] == records[1]["prepared_pdb_sha256"]


def test_unknown_generated_provenance_is_refused_without_rewriting(tmp_path):
    from benchmarks.competitors.run_matrix import _canonicalize_owned_reference

    path = tmp_path / "unknown.pdb"
    path.write_bytes(
        b"REMARK Unknown writer with scientific source evidence\nATOM ...\n"
    )
    original = path.read_bytes()
    with pytest.raises(RuntimeError, match="require review"):
        _canonicalize_owned_reference(path)
    assert path.read_bytes() == original


def test_owned_writer_block_normalizes_long_versions_without_losing_science(
    tmp_path, monkeypatch
):
    import molsysmt as msm
    from benchmarks.competitors.run_matrix import _canonicalize_owned_reference

    source = msm.convert(msm.systems["alanine dipeptide"]["alanine_dipeptide.h5msm"])
    writer = importlib.import_module("molsysmt.form.molsysmt_MolSys.to_string_pdb_text")
    prepared = []
    try:
        for n, version in enumerate(["0+unknown", "1.0.0rc1+" + "a" * 160]):
            monkeypatch.setattr(msm, "__version__", version)
            raw = writer.to_string_pdb_text(source).encode("ascii")
            path = tmp_path / f"generated-{n}.pdb"
            path.write_bytes(raw)
            record = _canonicalize_owned_reference(path)
            data = path.read_bytes()
            unchanged = data.splitlines(keepends=True)[
                record["prepared_provenance_record_count"] :
            ]
            restored = unchanged.copy()
            for index, text in sorted(
                record["original_records"].items(), key=lambda pair: int(pair[0])
            ):
                restored.insert(int(index), text.encode("ascii"))
            assert b"".join(restored) == raw
            assert record["raw_pdb_sha256"] == hashlib.sha256(raw).hexdigest()
            assert data.endswith(b"".join(unchanged))
            prepared.append(data)
    finally:
        monkeypatch.undo()
    assert prepared[0] == prepared[1]
