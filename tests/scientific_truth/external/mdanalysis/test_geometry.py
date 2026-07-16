"""External scientific agreement tests against MDAnalysis geometry kernels."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import Structures


pytest.importorskip("MDAnalysis")
from MDAnalysis.analysis.rms import rmsd
from MDAnalysis.lib.distances import calc_angles, calc_bonds, calc_dihedrals


def _structures(coordinates_nm, box_nm=None):
    unit = msm.pyunitwizard.unit("nm")
    box = None if box_nm is None else box_nm * unit
    return Structures(coordinates=coordinates_nm * unit, box=box)


def _values(quantity, unit):
    return msm.pyunitwizard.get_value(quantity, to_unit=unit)


def test_distances_agree_with_mdanalysis(
    rigid_geometry_coordinates_nm,
    external_float32_atol,
):
    """Compare pair distances without PBC using independently built inputs."""

    pairs = np.array([[0, 1], [0, 2]], dtype=np.int64)
    expected = np.stack(
        [calc_bonds(frame[pairs[:, 0]], frame[pairs[:, 1]]) for frame in rigid_geometry_coordinates_nm]
    )

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


def test_angles_agree_with_mdanalysis(
    rigid_geometry_coordinates_nm,
    external_float32_atol,
):
    """Compare geometric angles in radians without PBC."""

    triplets = np.array([[0, 1, 2], [0, 2, 3]], dtype=np.int64)
    expected = np.stack(
        [
            calc_angles(
                frame[triplets[:, 0]],
                frame[triplets[:, 1]],
                frame[triplets[:, 2]],
            )
            for frame in rigid_geometry_coordinates_nm
        ]
    )

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


def test_dihedrals_agree_with_mdanalysis(
    rigid_geometry_coordinates_nm,
    external_float32_atol,
):
    """Compare signed dihedral angles in radians without PBC."""

    quartets = np.array([[0, 1, 2, 3]], dtype=np.int64)
    expected = np.stack(
        [
            calc_dihedrals(
                frame[quartets[:, 0]],
                frame[quartets[:, 1]],
                frame[quartets[:, 2]],
                frame[quartets[:, 3]],
            )
            for frame in rigid_geometry_coordinates_nm
        ]
    )

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


def test_raw_and_least_rmsd_agree_with_mdanalysis(
    rigid_geometry_coordinates_nm,
    external_float32_atol,
):
    """Compare raw and optimally superposed RMSD values in nanometers."""

    reference = rigid_geometry_coordinates_nm[0]
    expected_raw = np.array(
        [rmsd(frame, reference, center=False, superposition=False) for frame in rigid_geometry_coordinates_nm]
    )
    expected_least = np.array(
        [rmsd(frame, reference, center=True, superposition=True) for frame in rigid_geometry_coordinates_nm]
    )
    structures = _structures(rigid_geometry_coordinates_nm)

    observed_raw = msm.structure.get_rmsd(
        structures,
        selection="all",
        reference_structure_index=0,
        heavy_mode="off",
        use_gpu=False,
    )
    observed_least = msm.structure.get_least_rmsd(
        structures,
        selection="all",
        reference_structure_index=0,
        use_gpu=False,
    )

    np.testing.assert_allclose(
        _values(observed_raw, "nm"),
        expected_raw,
        rtol=0.0,
        atol=external_float32_atol,
    )
    np.testing.assert_allclose(
        _values(observed_least, "nm"),
        expected_least,
        rtol=0.0,
        atol=external_float32_atol,
    )


def test_triclinic_minimum_image_distance_agrees_with_mdanalysis(
    triclinic_mic_case_nm,
    external_float32_atol,
):
    """Compare MIC distance in the canonical 60-degree row-vector cell."""

    coordinates, box = triclinic_mic_case_nm
    dimensions = np.array([2.0, 2.0, 3.0, 90.0, 90.0, 60.0])
    expected = calc_bonds(coordinates[[0]], coordinates[[1]], box=dimensions)

    observed = msm.structure.get_distances(
        _structures(coordinates[None, :, :], box[None, :, :]),
        selection=[0],
        selection_2=[1],
        pbc=True,
        heavy_mode="off",
        use_gpu=False,
    )

    np.testing.assert_allclose(
        np.ravel(_values(observed, "nm")),
        expected,
        rtol=0.0,
        atol=external_float32_atol,
    )
