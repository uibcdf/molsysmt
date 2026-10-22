"""Reject fast benchmark results that lost ownership, values or coverage."""

import json

import numpy as np
import pytest

from devtools.scripts import benchmark_native_copy as benchmark
from molsysmt import pyunitwizard as puw


def test_campaign_runs_an_isolated_production_worker(tmp_path):
    output = tmp_path / "campaign.json"
    benchmark.main(
        [
            "--case",
            "4x7",
            "--operation",
            "deferred_copy",
            "--repeats",
            "1",
            "--output",
            str(output),
        ]
    )
    report = json.loads(output.read_text())
    assert report["cases"][0]["operations"][0]["operation"] == "deferred_copy"
    assert report["cases"][0]["operations"][0]["source_geometry_bytes"] == 1176
    assert "molsysmt/interactions/result.py" in report["implementation_sha256"]


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
    clone.structures.set_coordinates(
        indices=[0],
        structure_indices=[3],
        value=puw.quantity([[[1.0, 2.0, 3.0]]], "nm"),
    )
    # Direct domain edits do not currently publish owner invalidation. The
    # benchmark must fail if it accidentally takes that unsupported shortcut.
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
