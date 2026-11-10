"""Exercise scientific-workload identity, provenance, repeats and dispositions."""

import json
from copy import deepcopy

import pytest

from benchmarks.compare_runs import compare_baselines
from devtools.tests.benchmark_fixtures import session


def compare(tmp_path, first, second, *, report_name="report.json"):
    paths = [tmp_path / "reference.json", tmp_path / "current.json"]
    for path, value in zip(paths, [first, second]):
        path.write_text(json.dumps(value))
    original = [path.read_bytes() for path in paths]
    target = tmp_path / report_name
    result = compare_baselines(*map(str, paths), report_path=target)
    assert [path.read_bytes() for path in paths] == original
    return result, json.loads(target.read_text())


def test_legacy_timings_are_unevaluable_even_when_identically_incomplete(
    tmp_path, capsys
):
    legacy = {"results": {"product": {"median_seconds": 1.0}}}
    code, report = compare(tmp_path, legacy, legacy)
    assert code == 1 and report["verdict"] == "unevaluable"
    assert not report["comparable"] and not report["comparisons"]
    assert "comparison_context" in report["reasons"][0]
    assert "PASS" not in capsys.readouterr().out


@pytest.mark.parametrize(
    "field,value",
    [("python", "3.13.14"), ("machine", "aarch64"), ("os_release", "different kernel")],
)
def test_different_runtime_is_not_a_product_regression(tmp_path, field, value):
    current = session(1.3)
    current["comparison_context"]["runtime"][field] = value
    code, report = compare(tmp_path, session(), current)
    assert code == 1 and not report["comparisons"] and not report["comparable"]


@pytest.mark.parametrize(
    "section,field,value",
    [
        ("hardware", "cpu_model", "other CPU"),
        ("hardware", "affinity_cpus", 1),
        ("limits", "cpu.max", "200000 100000"),
        ("limits", "memory.max", "4294967296"),
        ("threads", "OMP_NUM_THREADS", "4"),
        ("unit_policy", "standard_units", ["angstrom"]),
    ],
)
def test_resource_or_unit_changes_are_not_silently_compared(
    tmp_path, section, field, value
):
    current = session()
    current["comparison_context"][section][field] = value
    assert compare(tmp_path, session(), current)[0] == 1


@pytest.mark.parametrize(
    "section",
    [
        "runtime",
        "hardware",
        "limits",
        "threads",
        "dependencies",
        "environment_lock",
        "molsysmt_policy",
        "unit_policy",
    ],
)
@pytest.mark.parametrize("value", [None, [], {}])
def test_missing_or_malformed_context_is_not_equal_known_evidence(
    tmp_path, section, value
):
    value_session = session()
    value_session["comparison_context"][section] = value
    assert compare(tmp_path, value_session, value_session)[0] == 1


@pytest.mark.parametrize(
    "identity",
    [
        {"version": "1", "kind": "unavailable"},
        {"version": "1", "kind": "installed_record", "record_sha256": None},
        {"version": "1", "kind": "editable_git", "commit": "a" * 40, "dirty": True},
    ],
)
def test_unknown_or_dirty_dependency_cannot_certify_itself(tmp_path, identity):
    value = session()
    value["comparison_context"]["dependencies"]["mdtraj"] = identity
    assert compare(tmp_path, value, value)[0] == 1


@pytest.mark.parametrize(
    "field,value", [("git_commit", None), ("git_dirty", True), ("git_dirty", None)]
)
def test_uncertain_product_source_is_unevaluable(tmp_path, field, value):
    value_session = session()
    value_session["environment"][field] = value
    assert compare(tmp_path, value_session, value_session)[0] == 1


@pytest.mark.parametrize(
    "section,field,value",
    [
        ("inputs", "n_structures", 4),
        ("inputs", "n_atoms", 10),
        ("inputs", "files", {"coordinates": "f" * 64}),
        ("semantics", "pbc", True),
        ("semantics", "superposition", True),
        ("route", "input_dtype", "float32"),
        ("route", "output", "different payload"),
    ],
)
def test_same_name_cannot_hide_a_different_actual_workload(
    tmp_path, section, field, value
):
    current = session()
    current["results"]["product"]["workload"][section][field] = value
    code, report = compare(tmp_path, session(), current)
    assert code == 1 and "workload" in report["reasons"][0]


@pytest.mark.parametrize(
    "field,value",
    [
        ("samples_seconds", [1.0]),
        ("samples_seconds", [1.0, float("nan"), 1.0]),
        ("samples_seconds", [1.0, True, 1.0]),
        ("median_seconds", 1.2),
        ("repeats", 4),
        ("repeats", 3.0),
        ("iterations", 0),
    ],
)
def test_raw_repetitions_and_summaries_must_agree(tmp_path, field, value):
    current = session()
    current["results"]["product"][field] = value
    assert compare(tmp_path, session(), current)[0] == 1


def test_product_change_is_allowed_but_not_provider_or_measurement_change(tmp_path):
    first, current = session(), session(1.2)
    current["environment"] = {"git_commit": "f" * 40, "git_dirty": False}
    code, report = compare(tmp_path, first, current)
    assert code == 0 and report["verdict"] == "warning" and report["advisory"]
    current["comparison_context"]["dependencies"]["numpy"]["record_sha256"] = "e" * 64
    assert compare(tmp_path, first, current)[0] == 1
    current = session()
    current["results"]["product"]["measurement"]["harness_sha256"] = "e" * 64
    assert compare(tmp_path, first, current)[0] == 1


def test_new_unreferenced_paths_keep_the_whole_audit_partial(tmp_path):
    current = session()
    current["results"]["new"] = deepcopy(current["results"]["product"])
    code, report = compare(tmp_path, session(), current)
    assert code == 1 and report["verdict"] == "partial"
    assert report["unassessed_paths"] == ["new"] and len(report["comparisons"]) == 1


def test_variation_is_visible_without_claiming_statistical_confidence(tmp_path):
    current = session(1.2)
    current["results"]["product"]["samples_seconds"] = [0.5, 1.2, 2.0]
    code, report = compare(tmp_path, session(), current)
    assert code == 0 and report["verdict"] == "warning"
    assert report["comparisons"][0]["consistent_in_observed_ranges"] is False


@pytest.mark.parametrize("destination", ["reference.json", "current.json"])
def test_report_cannot_overwrite_either_input(tmp_path, destination):
    paths = [tmp_path / "reference.json", tmp_path / "current.json"]
    for path in paths:
        path.write_text(json.dumps(session()))
    original = [path.read_bytes() for path in paths]
    assert compare_baselines(*map(str, paths), report_path=tmp_path / destination) == 1
    assert [path.read_bytes() for path in paths] == original


def test_imported_module_and_package_manifest_cannot_be_omitted_or_forged(tmp_path):
    for field, value in [("origin_matches", False), ("module_sha256", None)]:
        current = session()
        current["comparison_context"]["dependencies"]["numpy"][field] = value
        assert compare(tmp_path, current, current)[0] == 1
    current = session()
    current["comparison_context"]["environment_lock"]["records"][0]["version"] = (
        "changed"
    )
    assert compare(tmp_path, current, current)[0] == 1
