"""External scientific agreement tests against MDTraj geometry kernels."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import Structures


md = pytest.importorskip("mdtraj")


def _structures(coordinates_nm, box_nm=None):
    unit = msm.pyunitwizard.unit("nm")
    box = None if box_nm is None else box_nm * unit
    return Structures(coordinates=coordinates_nm * unit, box=box)


def _values(quantity, unit):
    return msm.pyunitwizard.get_value(quantity, to_unit=unit)


def test_distances_agree_with_mdtraj(
    rigid_geometry_coordinates_nm,
    external_float32_atol,
):
    """Compare pair distances without PBC using independently built inputs."""

    pairs = np.array([[0, 1], [0, 2]], dtype=np.int64)
    trajectory = md.Trajectory(rigid_geometry_coordinates_nm.copy(), topology=None)
    expected = md.compute_distances(trajectory, pairs, periodic=False, opt=False)

    observed = msm.structure.get_distances(
        _structures(rigid_geometry_coordinates_nm),
        selection=pairs,
        pairs=True,
        pbc=False,
        heavy_mode="off",
        use_gpu=False,
    )

    np.testing.assert_allclose(
        _values(observed, "nm"),
        expected,
        rtol=0.0,
        atol=external_float32_atol,
    )


def test_angles_agree_with_mdtraj(
    rigid_geometry_coordinates_nm,
    external_float32_atol,
):
    """Compare geometric angles in radians without PBC."""

    triplets = np.array([[0, 1, 2], [0, 2, 3]], dtype=np.int64)
    trajectory = md.Trajectory(rigid_geometry_coordinates_nm.copy(), topology=None)
    expected = md.compute_angles(trajectory, triplets, periodic=False, opt=False)

    observed = msm.structure.get_angles(
        _structures(rigid_geometry_coordinates_nm),
        triplets,
        pbc=False,
        use_gpu=False,
    )

    np.testing.assert_allclose(
        _values(observed, "radians"),
        expected,
        rtol=0.0,
        atol=external_float32_atol,
    )


def test_dihedrals_agree_with_mdtraj(
    rigid_geometry_coordinates_nm,
    external_float32_atol,
):
    """Compare signed dihedral angles in radians without PBC."""

    quartets = np.array([[0, 1, 2, 3]], dtype=np.int64)
    trajectory = md.Trajectory(rigid_geometry_coordinates_nm.copy(), topology=None)
    expected = md.compute_dihedrals(trajectory, quartets, periodic=False, opt=False)

    observed = msm.structure.get_dihedral_angles(
        _structures(rigid_geometry_coordinates_nm),
        dihedral_quartets=quartets,
        pbc=False,
        use_gpu=False,
    )

    np.testing.assert_allclose(
        _values(observed, "radians"),
        expected,
        rtol=0.0,
        atol=external_float32_atol,
    )


def test_least_rmsd_agrees_with_mdtraj_for_a_rigid_transform(
    rigid_geometry_coordinates_nm,
    external_float32_atol,
):
    """Compare optimally superposed RMSD values in nanometers."""

    query = md.Trajectory(rigid_geometry_coordinates_nm.copy(), topology=None)
    reference = md.Trajectory(rigid_geometry_coordinates_nm[[0]].copy(), topology=None)
    expected = md.rmsd(query, reference, frame=0, parallel=False)

    observed = msm.structure.get_least_rmsd(
        _structures(rigid_geometry_coordinates_nm),
        selection="all",
        reference_structure_index=0,
        use_gpu=False,
    )

    np.testing.assert_allclose(
        _values(observed, "nm"),
        expected,
        rtol=0.0,
        atol=external_float32_atol,
    )


def test_triclinic_minimum_image_distance_agrees_with_mdtraj(
    triclinic_mic_case_nm,
    external_float32_atol,
):
    """Compare MIC distance in the canonical 60-degree row-vector cell."""

    coordinates, box = triclinic_mic_case_nm
    trajectory = md.Trajectory(coordinates[None, :, :].copy(), topology=None)
    trajectory.unitcell_vectors = box[None, :, :]
    expected = md.compute_distances(
        trajectory,
        np.array([[0, 1]], dtype=np.int64),
        periodic=True,
        opt=False,
    )

    observed = msm.structure.get_distances(
        _structures(coordinates[None, :, :], box[None, :, :]),
        selection=[0],
        selection_2=[1],
        pbc=True,
        heavy_mode="off",
        use_gpu=False,
    )

    np.testing.assert_allclose(
        np.squeeze(_values(observed, "nm"), axis=-1),
        expected,
        rtol=0.0,
        atol=external_float32_atol,
    )
