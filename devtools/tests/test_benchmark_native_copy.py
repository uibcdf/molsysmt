"""Reject fast benchmark results that lost ownership, values or coverage."""

import json

import numpy as np
import pytest

from devtools.scripts import benchmark_native_copy as benchmark
from molsysmt import pyunitwizard as puw


@pytest.mark.parametrize("workload", ["baseline", "mutable_observables"])
def test_campaign_runs_an_isolated_production_worker(tmp_path, workload):
    output = tmp_path / "campaign.json"
    benchmark.main(
        [
            "--case",
            "4x7",
            "--operation",
            "deferred_copy",
            "--repeats",
            "1",
            "--workload",
            workload,
            "--output",
            str(output),
        ]
    )
    report = json.loads(output.read_text())
    assert report["cases"][0]["operations"][0]["operation"] == "deferred_copy"
    assert report["cases"][0]["operations"][0]["source_geometry_bytes"] == 1176
    assert "molsysmt/interactions/result.py" in report["implementation_sha256"]
    assert report["workload"] == workload
    assert report["cases"][0]["operations"][0]["source_mutable_array_bytes"] == (
        1344 if workload == "mutable_observables" else 0
    )


@pytest.mark.parametrize("operation", benchmark._OPERATIONS)
def test_production_operations_validate_real_results(operation):
    result = benchmark._worker(4, 7, operation, repeats=1, chunk=2)
    assert result["median_seconds"] >= 0
    assert result["traced_operation_peak_bytes"] > 0
    assert len(result["samples"]) == 1
    original_bytes = (7 * 4 * 3 + 7 * 3 * 3) * 8
    assert result["source_geometry_bytes"] == original_bytes
    if operation == "deferred_copy":
        assert result["source_and_result_unique_geometry_bytes"] == original_bytes
    elif operation in ("eager_copy", "h5msm_read"):
        assert result["source_and_result_unique_geometry_bytes"] == 2 * original_bytes
    elif operation.startswith("edit_"):
        assert (
            result["source_and_result_unique_geometry_bytes"]
            == original_bytes + 7 * 4 * 3 * 8
        )
    if operation.startswith("h5msm_"):
        assert result["file_bytes"] > 0


def test_validator_rejects_stale_coverage_and_wrong_coordinates():
    source = benchmark._fixture(4, 7)
    clone = source.copy(deep=False)
    old_analysis = clone.interactions["pairs"]
    clone.structures.set_coordinates(
        indices=[0],
        structure_indices=[3],
        value=puw.quantity([[[1.0, 2.0, 3.0]]], "nm"),
    )
    benchmark._check_system(clone, 4, 7, edited=[3])
    # Deliberately restore stale evidence to check the validator's intent.
    clone.interactions = {"pairs": old_analysis}
    with pytest.raises(AssertionError):
        benchmark._check_system(clone, 4, 7, edited=[3])
    clone.interactions = {
        "pairs": clone.interactions["pairs"].invalidate_structures([3])
    }
    benchmark._check_system(clone, 4, 7, edited=[3])
    with pytest.raises(AssertionError):
        benchmark._check_system(clone, 4, 7)
    np.testing.assert_allclose(
        puw.get_value(
            source.structures.get_coordinates(indices=[0], structure_indices=[3]),
            to_unit="nm",
        ),
        [[[0.00036, 0.00037, 0.00038]]],
        rtol=1e-15,
        atol=0,
    )


@pytest.mark.parametrize("case", ["0x3", "3x2", "3x4x5", "not-a-size"])
def test_bad_sizes_are_rejected_before_launching_workers(case, tmp_path):
    with pytest.raises(SystemExit, match="2"):
        benchmark.main(["--case", case, "--output", str(tmp_path / "unused.json")])


@pytest.mark.parametrize("workload", ["mutable_observables", "many_interactions"])
@pytest.mark.parametrize("operation", benchmark._COPY_EDIT_OPERATIONS)
def test_extended_workloads_copy_and_edit_independent_real_payloads(
    workload, operation
):
    report = benchmark._worker(16, 7, operation, 1, 2, workload)
    if workload == "mutable_observables":
        assert report["source_mutable_array_bytes"] == 5376
        assert report["source_and_result_unique_mutable_array_bytes"] == 10752
    else:
        assert report["source_analyses"]["reused"]["relations"] == 128
        assert report["source_analyses"]["changing"]["relations"] == 240
        assert report["source_analyses"]["changing"]["occurrences"] == 768


def test_extended_validation_rejects_corrupt_observables_and_stale_busy_coverage():
    mutable = benchmark._fixture(4, 7, "mutable_observables")
    clone = mutable.copy(deep=False)
    clone.structures._velocities[0, 0, 0] = 2.0
    with pytest.raises(AssertionError):
        benchmark._check_workload(clone, 4, 7, "mutable_observables")
    assert mutable.structures._velocities[0, 0, 0] == 1.0
    busy = benchmark._fixture(16, 7, "many_interactions")
    with pytest.raises(AssertionError):
        benchmark._check_workload(busy, 16, 7, "many_interactions", edited=[0])


def test_warming_indexes_records_the_additional_numeric_cache():
    cold = benchmark._worker(16, 7, "deferred_copy", 1, 2, "many_interactions")
    warm = benchmark._worker(16, 7, "deferred_copy", 1, 2, "many_interactions", True)
    assert (
        warm["source_analyses"]["changing"]["numeric_bytes"]
        > cold["source_analyses"]["changing"]["numeric_bytes"]
    )


@pytest.mark.parametrize(
    "options",
    [
        ["--workload", "mutable_observables", "--operation", "h5msm_read"],
        ["--warm-atom-index"],
    ],
)
def test_unsupported_profile_operations_are_refused_before_workers(tmp_path, options):
    with pytest.raises(SystemExit, match="2"):
        benchmark.main(["--output", str(tmp_path / "unused.json"), *options])
