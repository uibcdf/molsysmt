"""Check evidence production against the actual runtime, rather than schema shape."""

import hashlib
import importlib.metadata
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from benchmarks import telemetry
from benchmarks.compare_runs import compare_baselines
from benchmarks.harness import BenchmarkHarness, save_session_results
from devtools.tests.benchmark_fixtures import session


def test_array_fingerprint_includes_values_dimensions_and_precision():
    first = np.arange(12, dtype=np.float64).reshape(2, 2, 3)
    identity = telemetry.array_identity(first)
    assert identity["sha256"] == hashlib.sha256(first.tobytes()).hexdigest()
    assert identity["shape"] == [2, 2, 3]
    assert telemetry.array_identity(first.astype(np.float32)) != identity
    with pytest.raises(ValueError):
        telemetry.array_identity(first[:, ::-1])


def test_provider_identity_binds_actual_initializer_to_distribution(
    monkeypatch, tmp_path
):
    identity = telemetry._dependency_identity("numpy")
    assert identity["origin_matches"] is True
    assert (
        identity["module_sha256"]
        == hashlib.sha256(Path(np.__file__).read_bytes()).hexdigest()
    )
    foreign = tmp_path / "foreign.py"
    foreign.write_text("# Foreign module with a matching declared version.\n")
    monkeypatch.setattr(
        telemetry.importlib,
        "import_module",
        lambda name: SimpleNamespace(__file__=str(foreign), __version__=np.__version__),
    )
    assert telemetry._dependency_identity("numpy")["origin_matches"] is False


def test_environment_lock_has_the_actual_package_inventory():
    lock = telemetry._environment_lock()
    assert lock["records"]
    encoded = json.dumps(
        lock["records"], sort_keys=True, separators=(",", ":")
    ).encode()
    assert lock["sha256"] == hashlib.sha256(encoded).hexdigest()
    assert "molsysmt" not in {entry["name"] for entry in lock["records"]}
    if lock["kind"] == "conda_records":
        import sys

        expected = [
            json.loads(p.read_text())
            for p in (Path(sys.prefix) / "conda-meta").glob("*.json")
        ]
        expected = {
            value["name"]: value
            for value in expected
            if value.get("name") != "molsysmt"
        }
        assert len(lock["records"]) == len(expected)
        assert all(
            value["build"] == expected[value["name"]]["build"]
            for value in lock["records"]
        )
    else:
        assert len(lock["records"]) == sum(
            value.metadata.get("Name", "").lower().replace("_", "-") != "molsysmt"
            for value in importlib.metadata.distributions()
        )


@pytest.mark.parametrize("value", [True, 0, -1, 1.5])
def test_invalid_harness_counts_are_rejected_before_fork(value):
    with pytest.raises(ValueError):
        BenchmarkHarness("invalid", iterations=value)
    with pytest.raises(ValueError):
        BenchmarkHarness("invalid", repeats=value)


def test_duplicate_or_empty_cases_cannot_disappear_during_serialization(tmp_path):
    for results in [[], [{"name": "duplicate"}, {"name": "duplicate"}]]:
        target = tmp_path / "result.json"
        with pytest.raises(ValueError):
            save_session_results("invalid", results, str(target))
        assert not target.exists()


def test_diagnostic_report_failure_preserves_prior_report_and_inputs(
    tmp_path, monkeypatch
):
    first, second, report = [
        tmp_path / name for name in ["first.json", "second.json", "report.json"]
    ]
    for path in [first, second]:
        path.write_text(json.dumps(session()))
    report.write_text("ORIGINAL_REPORT")
    before = {path: path.read_bytes() for path in [first, second, report]}
    import benchmarks.compare_runs as module

    def fail(*args):
        raise OSError("controlled publication failure")

    monkeypatch.setattr(module.os, "replace", fail)
    assert compare_baselines(str(first), str(second), report_path=report) == 1
    assert before == {path: path.read_bytes() for path in before}
    assert set(tmp_path.iterdir()) == set(before)
