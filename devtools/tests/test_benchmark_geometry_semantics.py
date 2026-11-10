"""Require actual common observables before comparing geometry timings."""

import numpy as np
import pytest

import molsysmt as msm
from benchmarks.competitors import test_geometry as suite


@pytest.fixture(name="geometry_input")
def geometry_input_fixture(tmp_path):
    mdtraj = pytest.importorskip("mdtraj")
    pytest.importorskip("MDAnalysis")
    topology = mdtraj.Topology()
    chain = topology.add_chain()
    for index in range(4):
        group = topology.add_residue("ALA", chain, resSeq=index + 1)
        topology.add_atom("CA", mdtraj.element.carbon, group)
    first = np.array(
        [
            [0.05, 0.05, 0.05],
            [0.15, 0.05, 0.05],
            [0.05, 0.25, 0.05],
            [0.05, 0.05, 0.95],
        ],
        dtype=np.float32,
    )
    xyz = np.stack([first, first + [2.0, 0, 0], first.copy()]).astype(np.float32)
    xyz[2, 1, 1] += 0.1
    trajectory = mdtraj.Trajectory(
        xyz,
        topology,
        unitcell_lengths=np.ones((3, 3)),
        unitcell_angles=np.full((3, 3), 90),
    )
    path = tmp_path / "geometry.pdb"
    trajectory.save_pdb(path)
    # PDB quantization is part of the shared actual input, outside timing.
    reference = mdtraj.load(path).xyz.astype(np.float64)
    return reference, path


@pytest.fixture(params=["nm", "angstrom"])
def geometry_observations(geometry_input, monkeypatch, request):
    reference, path = geometry_input
    observations = {}

    def observe(self, warmup_func, timed_func):
        value = timed_func()
        if msm.pyunitwizard.is_quantity(value):
            value = msm.pyunitwizard.get_value(value, to_unit="nm")
        else:
            value = np.asarray(value)
            if self.name.endswith("mdanalysis"):
                value = value / 10
        observations[self.name] = np.asarray(value)
        return {"name": self.name, "median_seconds": 1.0, "peak_rss_mb": 0.0}

    monkeypatch.setattr(suite.BenchmarkHarness, "run", observe)
    with msm.pyunitwizard.context(standard_units=[request.param]):
        suite.run_geometry_benchmarks(str(path))
    return reference, observations


def test_every_reported_rmsd_is_unaligned_and_preserves_a_rigid_translation(
    geometry_observations,
):
    xyz, results = geometry_observations
    expected = np.sqrt(np.mean(np.sum((xyz - xyz[0]) ** 2, axis=-1), axis=-1))
    assert expected[1] == pytest.approx(2.0)
    for name, value in results.items():
        if "rmsd" in name:
            np.testing.assert_allclose(
                value.reshape(-1), expected, atol=2e-6, rtol=0, err_msg=name
            )


def test_every_reported_distance_uses_no_periodic_images_and_the_full_pair_grid(
    geometry_observations,
):
    xyz, results = geometry_observations
    expected = np.linalg.norm(xyz[:, :, None] - xyz[:, None, :], axis=-1)
    assert expected[0, 0, 3] == pytest.approx(0.9)
    for name, value in results.items():
        if "distances" in name:
            assert value.shape == expected.shape, name
            np.testing.assert_allclose(value, expected, atol=2e-6, rtol=0, err_msg=name)


def test_incorrect_external_result_stops_before_any_timing(geometry_input, monkeypatch):
    mdtraj = pytest.importorskip("mdtraj")
    _, path = geometry_input
    timed = []
    monkeypatch.setattr(mdtraj, "rmsd", lambda *a, **kw: np.zeros(3))
    monkeypatch.setattr(
        suite.BenchmarkHarness, "run", lambda *a, **kw: timed.append(True)
    )
    with pytest.raises(AssertionError):
        suite.run_geometry_benchmarks(str(path))
    assert not timed
