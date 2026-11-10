"""Keep timing warnings advisory and malformed evidence visibly unevaluable."""

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
    "current,warns",
    [(0.7, False), (1.0, False), (1.1, False), (1.15, False), (1.16, True)],
)
def test_real_improvements_and_regressions_keep_the_advisory_threshold(
    tmp_path, capsys, current, warns
):
    assert compare(tmp_path, session(), session(current)) == 0
    output = capsys.readouterr().out
    assert ("WARNING: TIMING DIFFERENCES" in output) is warns
    assert "PASS:" not in output


@pytest.mark.parametrize("name", ["product", "competitor_center_mdtraj"])
def test_product_and_third_party_slowdowns_warn_without_blocking(
    tmp_path, capsys, name
):
    assert (
        compare(
            tmp_path,
            session(name=name),
            session(1.3211, name=name),
        )
        == 0
    )
    output = capsys.readouterr().out
    assert "WARNING: TIMING DIFFERENCES" in output and name in output
    assert "comparability is not established" in output
    assert "improvement issue" in output


def test_invalid_json_fails_without_overwriting_the_reference(tmp_path):
    path = tmp_path / "invalid.json"
    path.write_text("{not-json")
    assert compare_baselines(str(path), str(path)) == 1
    assert path.read_text() == "{not-json"
