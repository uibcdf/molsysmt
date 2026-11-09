"""Require meaningful storage observations before reporting benchmark timings."""

import json

import pytest

from devtools.scripts import benchmark_h5msm_mechanics as benchmark


def test_public_campaign_validates_all_operations_in_fresh_workers(tmp_path):
    output = tmp_path / "measurements.json"
    benchmark.main(["--case", "4x7", "--repeats", "1", "--output", str(output)])
    report = json.loads(output.read_text())
    operations = report["cases"][0]["operations"]
    assert [item["operation"] for item in operations] == list(benchmark._OPERATIONS)
    assert len({item["file_bytes"] for item in operations}) == 1
    datasets = operations[0]["datasets"]
    assert datasets["structures/coordinates"]["shape"] == [7, 4, 3]
    assert any(
        name.startswith("molecular_mechanics/snapshot/arrays/") for name in datasets
    )
    for item in operations:
        assert len(item["samples_seconds"]) == 1
        assert item["traced_operation_peak_bytes"] > 0


@pytest.mark.parametrize("damage", ["values", "dtype", "producer", "history", "unit"])
def test_validator_refuses_corrupted_evidence_instead_of_reporting_fast_results(damage):
    system = benchmark._mechanical_fixture(4, 7)
    mechanics = system.molecular_mechanics
    if damage == "values":
        mechanics.atoms_ff.loc[0, "partial_charge"] = 0
    elif damage == "dtype":
        mechanics.atoms_ff["formal_charge"] = mechanics.atoms_ff[
            "formal_charge"
        ].astype("Int64")
    elif damage == "producer":
        mechanics.partial_charge_assignment["software"]["fixture"] = "wrong"
    elif damage == "history":
        mechanics.atom_type_assignment["history"] = ["synthetic storage only"]
    else:
        mechanics.cutoff_distance = benchmark.puw.quantity(12.0, "nm")
    with pytest.raises(AssertionError):
        benchmark._check_mechanics(mechanics, 4)


@pytest.mark.parametrize("case", ["0x4", "4x2", "4x7x8", "bad", "100000x100"])
def test_invalid_or_over_budget_sizes_refuse_before_launching_workers(case, tmp_path):
    with pytest.raises(SystemExit, match="2"):
        benchmark.main(["--case", case, "--output", str(tmp_path / "unused.json")])
