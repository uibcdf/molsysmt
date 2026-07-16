"""Curated scientific agreement tests for periodic pentaalanine."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import Structures


md = pytest.importorskip("mdtraj")


FRAME_INDICES = np.array([0, 499, 999, 2499, 4999], dtype=np.int64)
CA_INDICES = np.array([8, 18, 28, 38, 48], dtype=np.int64)
MIC_PAIRS = np.array([[0, 61], [8, 50], [19, 42], [6, 55]], dtype=np.int64)
PHI_QUARTETS = np.array(
    [[4, 6, 8, 14], [24, 26, 28, 34], [44, 46, 48, 54]],
    dtype=np.int64,
)


@pytest.fixture(scope="module")
def pentalanine_readers(pentalanine_trajectory_paths):
    """Load representative frames from paired HDF5 and H5MSM artifacts."""

    mdtraj_path, h5msm_path = pentalanine_trajectory_paths
    trajectory = md.load(mdtraj_path)[FRAME_INDICES]
    coordinates, box, time = msm.get(
        h5msm_path,
        element="atom",
        structure_indices=FRAME_INDICES,
        coordinates=True,
        box=True,
        time=True,
    )
    coordinates = msm.pyunitwizard.get_value(coordinates, to_unit="nm")
    box = msm.pyunitwizard.get_value(box, to_unit="nm")
    time = msm.pyunitwizard.get_value(time, to_unit="ps")
    structures = Structures(
        coordinates=coordinates * msm.pyunitwizard.unit("nm"),
        box=box * msm.pyunitwizard.unit("nm"),
        time=time * msm.pyunitwizard.unit("ps"),
    )
    return trajectory, coordinates, box, time, structures


def test_pentalanine_artifacts_agree_on_coordinates_box_and_time(
    pentalanine_readers,
    external_float32_atol,
):
    """Validate paired trajectory artifacts before comparing analyses."""

    trajectory, coordinates, box, time, _ = pentalanine_readers

    assert trajectory.n_frames == len(FRAME_INDICES)
    assert trajectory.n_atoms == 62
    assert trajectory.n_residues == 7
    np.testing.assert_allclose(coordinates, trajectory.xyz, rtol=0.0, atol=external_float32_atol)
    np.testing.assert_allclose(box, trajectory.unitcell_vectors, rtol=0.0, atol=external_float32_atol)
    np.testing.assert_allclose(time, trajectory.time, rtol=0.0, atol=external_float32_atol)


def test_pentalanine_periodic_distances_agree_with_mdtraj(
    pentalanine_readers,
    external_float32_atol,
):
    """Compare MIC distances for atom pairs that cross the periodic boundary."""

    trajectory, _, _, _, structures = pentalanine_readers
    expected = md.compute_distances(trajectory, MIC_PAIRS, periodic=True, opt=False)
    observed = msm.structure.get_distances(
        structures,
        selection=MIC_PAIRS,
        pairs=True,
        pbc=True,
        heavy_mode="off",
        use_gpu=False,
    )
    observed = msm.pyunitwizard.get_value(observed, to_unit="nm")

    np.testing.assert_allclose(observed, expected, rtol=0.0, atol=external_float32_atol)


def test_pentalanine_periodic_phi_dihedrals_agree_with_mdtraj(
    pentalanine_readers,
    external_float32_atol,
):
    """Compare signed backbone angles using the periodic minimum image."""

    trajectory, _, _, _, structures = pentalanine_readers
    expected = md.compute_dihedrals(
        trajectory,
        PHI_QUARTETS,
        periodic=True,
        opt=False,
    )
    observed = msm.structure.get_dihedral_angles(
        structures,
        dihedral_quartets=PHI_QUARTETS,
        pbc=True,
        use_gpu=False,
    )
    observed = msm.pyunitwizard.get_value(observed, to_unit="radians")

    np.testing.assert_allclose(observed, expected, rtol=0.0, atol=external_float32_atol)


def test_pentalanine_ca_least_rmsd_agrees_with_mdtraj(
    pentalanine_readers,
    external_float32_atol,
):
    """Compare C-alpha least-RMSD across distributed trajectory frames."""

    trajectory, coordinates, _, _, _ = pentalanine_readers
    expected = md.rmsd(
        md.Trajectory(trajectory.xyz[:, CA_INDICES, :].copy(), topology=None),
        md.Trajectory(trajectory.xyz[[0]][:, CA_INDICES, :].copy(), topology=None),
        frame=0,
        parallel=False,
    )
    structures = Structures(
        coordinates=coordinates[:, CA_INDICES, :] * msm.pyunitwizard.unit("nm")
    )
    observed = msm.structure.get_least_rmsd(
        structures,
        selection="all",
        reference_structure_index=0,
        use_gpu=False,
    )
    observed = msm.pyunitwizard.get_value(observed, to_unit="nm")

    # Identity is governed by the analytic oracle RMSD(x, x) = 0. MDTraj's
    # float32 QCP path reports about 1.5e-4 nm for this five-atom self-match.
    np.testing.assert_allclose(observed[0], 0.0, rtol=0.0, atol=1.0e-12)
    np.testing.assert_allclose(
        observed[1:],
        expected[1:],
        rtol=0.0,
        atol=external_float32_atol,
    )
