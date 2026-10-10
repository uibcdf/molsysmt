"""Keep startup evidence distinct from warm conversion and provider metadata."""

import hashlib
import json
import subprocess
import sys

import pytest

from devtools.scripts import benchmark_form_registry_startup as benchmark


@pytest.mark.parametrize("mode", ["conversion", "validation"])
def test_measurements_use_fresh_workers_and_keep_warm_routes_distinct(mode):
    source = benchmark.ROOT / "molsysmt/data/pdb/181l.pdb"
    original = source.read_bytes()
    run = subprocess.run(
        [sys.executable, benchmark.__file__, "--mode", mode, "--trials", "2"],
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )
    assert run.returncode == 0, run.stderr + run.stdout
    record = json.loads(run.stdout)
    assert record["input_sha256"] == hashlib.sha256(original).hexdigest()
    assert source.read_bytes() == original
    assert record["mode"] == mode
    samples = record["samples"]
    assert len(samples) == 2
    for sample in samples:
        # Namespaced runtimes can report the same PID for independent workers.
        # Each sample must start before any form implementation is imported.
        assert sample["initial_form_modules"] == []
        assert sample["n_atoms"] == 1441
        assert {"coordinates", "bonded_atom_pairs", "formal_charge", "atom_id"} <= set(
            sample["parity_checked"]
        )
        assert sample["software"]["depdigest"]["distribution_version"]
        assert "source" in sample["software"]["depdigest"]
        assert sample["conversion_added_form_modules"] > 0
        assert sample["repeated_conversion_seconds"] >= 0
        assert sample["prepared_conversion_seconds"] >= 0
        if mode == "conversion":
            assert sample["first_conversion_seconds"] > 0
            assert "target_validation_seconds" not in sample
            assert "conversion_after_validation_seconds" not in sample
            assert "scan_seconds" not in sample
        else:
            assert sample["target_validation_seconds"] > 0
            assert sample["conversion_after_validation_seconds"] > 0
            assert "first_conversion_seconds" not in sample
            assert "scan_seconds" in sample
    for name, observed in record["median_seconds"].items():
        assert observed == (samples[0][name] + samples[1][name]) / 2


def test_invalid_measurement_input_fails_without_a_success_record(tmp_path):
    run = subprocess.run(
        [sys.executable, benchmark.__file__, "--input", str(tmp_path / "missing.pdb")],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert run.returncode != 0
    assert run.stdout == ""
    assert "existing local file" in run.stderr
