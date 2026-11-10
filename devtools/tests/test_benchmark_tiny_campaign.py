"""Receive real benchmark production/reading on a deliberately tiny workload."""

import json
from pathlib import Path

import pytest

import molsysmt as msm
from benchmarks.comparability import validate_measurement
from benchmarks.compare_runs import compare_baselines
from benchmarks.competitors import run_matrix
from benchmarks.harness import BenchmarkHarness
from devtools.tests.test_benchmark_geometry_semantics import (
    geometry_input_fixture,  # noqa: F401
)


def test_two_actual_tiny_campaigns_keep_scientific_and_context_evidence(
    geometry_input, tmp_path, monkeypatch
):
    mdtraj = pytest.importorskip("mdtraj")
    pytest.importorskip("MDAnalysis")
    _, pdb = geometry_input
    trajectory = mdtraj.load(pdb)
    h5 = tmp_path / "reference.h5"
    dcd = tmp_path / "reference.dcd"
    trajectory.save_hdf5(h5)
    trajectory.save_dcd(dcd)
    monkeypatch.setitem(
        msm.systems,
        "chicken villin HP35",
        {
            "traj_chicken_villin_HP35_solvated.h5": str(h5),
            "traj_chicken_villin_HP35_solvated.dcd": str(dcd),
        },
    )
    original_init = BenchmarkHarness.__init__

    def tiny_init(self, name, *args, **kwargs):
        kwargs.update(iterations=1, repeats=3)
        original_init(self, name, *args, **kwargs)

    monkeypatch.setattr(BenchmarkHarness, "__init__", tiny_init)
    snapshots = {p: p.read_bytes() for p in (pdb, h5, dcd)}
    paths = [tmp_path / "first.json", tmp_path / "second.json"]
    original_policy = msm.pyunitwizard.configure.report()
    for path in paths:
        run_matrix.main(["--output", str(path)])
    assert msm.pyunitwizard.configure.report() == original_policy
    assert snapshots == {p: p.read_bytes() for p in snapshots}
    sessions = [json.loads(p.read_text()) for p in paths]
    for value in sessions:
        assert len(value["results"]) == 21
        assert value["environment"]["native_backend_sha256"]
        assert set(value["resource_observations"]) == {"before", "after"}
        for name, entry in value["results"].items():
            validate_measurement(entry, name)
            assert entry["iterations"] == 1 and entry["repeats"] == 3
            assert entry["workload"]["inputs"]["n_atoms"] == 4
            assert entry["workload"]["inputs"]["n_structures"] == 3
    target = tmp_path / "comparison.json"
    code = compare_baselines(*map(str, paths), report_path=target)
    report = json.loads(target.read_text())
    clean = all(value["environment"]["git_dirty"] is False for value in sessions)
    assert code == (0 if clean else 1), report
    assert report["comparable"] is clean
    if clean:
        assert len(report["comparisons"]) == 21
    else:
        assert "clean committed input" in report["reasons"][0]
    # These raw tiny timing samples test evidence transport, not a speed ranking.
    assert all(Path(path).read_bytes() == data for path, data in snapshots.items())
