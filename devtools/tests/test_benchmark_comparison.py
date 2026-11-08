"""Require timing evidence without waiving any existing numeric regressions."""

import json

import pytest

from benchmarks.compare_runs import compare_baselines


def compare(tmp_path, baseline, current, **kwargs):
    before = tmp_path / "baseline.json"
    after = tmp_path / "current.json"
    before.write_text(json.dumps(baseline))
    after.write_text(json.dumps(current))
    snapshots = [path.read_bytes() for path in (before, after)]
    code = compare_baselines(str(before), str(after), **kwargs)
    assert [path.read_bytes() for path in (before, after)] == snapshots
    return code


def session(value=1.0, name="product"):
    return {"results": {name: {"median_seconds": value}}}


@pytest.mark.parametrize("data", [{}, [], None, {"results": {}}, {"results": []}])
@pytest.mark.parametrize("side", ["reference", "current"])
def test_empty_or_malformed_sessions_cannot_pass(tmp_path, data, side):
    baseline, current = (data, session()) if side == "reference" else (session(), data)
    assert compare(tmp_path, baseline, current) == 1


@pytest.mark.parametrize(
    "value", [float("nan"), float("inf"), -float("inf"), 0, -1, True, None, "1.0", []]
)
@pytest.mark.parametrize("side", ["reference", "current"])
def test_invalid_medians_cannot_pass(tmp_path, value, side):
    baseline, current = (
        (session(value), session())
        if side == "reference"
        else (session(), session(value))
    )
    assert compare(tmp_path, baseline, current) == 1


@pytest.mark.parametrize("entry", [{}, [], None])
def test_missing_median_or_nonobject_record_cannot_pass(tmp_path, entry):
    assert compare(tmp_path, session(), {"results": {"product": entry}}) == 1


def test_current_run_cannot_omit_a_reference_measurement(tmp_path):
    baseline = {
        "results": {**session()["results"], **session(name="control")["results"]}
    }
    assert compare(tmp_path, baseline, session()) == 1
    assert compare(tmp_path, session(), session(name="new-path")) == 1


@pytest.mark.parametrize(
    "threshold", [float("nan"), float("inf"), -0.1, True, None, "0.15"]
)
def test_invalid_threshold_cannot_pass(tmp_path, threshold):
    assert compare(tmp_path, session(), session(), threshold=threshold) == 1


@pytest.mark.parametrize(
    "current,expected", [(0.7, 0), (1.0, 0), (1.1, 0), (1.15, 0), (1.16, 1)]
)
def test_real_improvements_and_regressions_keep_the_same_threshold(
    tmp_path, current, expected
):
    assert compare(tmp_path, session(), session(current)) == expected


def test_third_party_regression_remains_blocking_pending_owner_decision(tmp_path):
    assert (
        compare(
            tmp_path,
            session(name="competitor_center_mdtraj"),
            session(1.3211, name="competitor_center_mdtraj"),
        )
        == 1
    )


def test_invalid_json_fails_without_overwriting_the_reference(tmp_path):
    path = tmp_path / "invalid.json"
    path.write_text("{not-json")
    assert compare_baselines(str(path), str(path)) == 1
    assert path.read_text() == "{not-json"
