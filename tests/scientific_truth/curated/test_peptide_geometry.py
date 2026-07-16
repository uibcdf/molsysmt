"""Scientific agreement tests on curated peptide systems."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import systems


md = pytest.importorskip("mdtraj")
pytest.importorskip("MDAnalysis")
import MDAnalysis as mda
from MDAnalysis.lib.distances import calc_angles, calc_bonds, calc_dihedrals


def _values(quantity, unit):
    return msm.pyunitwizard.get_value(quantity, to_unit=unit)


def _assert_angles_equivalent(observed, expected, atol):
    """Comparing angles modulo 2 pi at the signed branch cut."""

    difference = np.arctan2(np.sin(observed - expected), np.cos(observed - expected))
    np.testing.assert_allclose(difference, 0.0, rtol=0.0, atol=atol)


def test_met_enkephalin_backbone_geometry_agrees_with_both_oracles(
    external_float32_atol,
):
    """Compare real peptide bonds, angles, and signed dihedrals."""

    path = systems["Met-enkephalin"]["met_enkephalin.pdb"]
    pairs = np.array([[0, 2], [2, 19], [19, 21], [21, 23]], dtype=np.int64)
    triplets = np.array([[0, 2, 19], [2, 19, 21]], dtype=np.int64)
    quartets = np.array([[0, 2, 19, 21], [2, 19, 21, 23]], dtype=np.int64)

    trajectory = md.load(str(path))
    universe = mda.Universe(str(path))
    coordinates_angstrom = universe.atoms.positions

    assert [trajectory.topology.atom(index).name for index in [0, 2, 19, 21, 23]] == [
        "N",
        "CA",
        "C",
        "N",
        "CA",
    ]
    assert universe.atoms[[0, 2, 19, 21, 23]].names.tolist() == ["N", "CA", "C", "N", "CA"]

    expected_distances_mdtraj = md.compute_distances(
        trajectory,
        pairs,
        periodic=False,
        opt=False,
    )
    expected_angles_mdtraj = md.compute_angles(
        trajectory,
        triplets,
        periodic=False,
        opt=False,
    )
    expected_dihedrals_mdtraj = md.compute_dihedrals(
        trajectory,
        quartets,
        periodic=False,
        opt=False,
    )
    expected_distances_mda = calc_bonds(
        coordinates_angstrom[pairs[:, 0]],
        coordinates_angstrom[pairs[:, 1]],
    )[None, :] / 10.0
    expected_angles_mda = calc_angles(
        coordinates_angstrom[triplets[:, 0]],
        coordinates_angstrom[triplets[:, 1]],
        coordinates_angstrom[triplets[:, 2]],
    )[None, :]
    expected_dihedrals_mda = calc_dihedrals(
        coordinates_angstrom[quartets[:, 0]],
        coordinates_angstrom[quartets[:, 1]],
        coordinates_angstrom[quartets[:, 2]],
        coordinates_angstrom[quartets[:, 3]],
    )[None, :]

    observed_distances = msm.structure.get_distances(
        path,
        selection=pairs,
        pairs=True,
        pbc=False,
        heavy_mode="off",
        use_gpu=False,
    )
    observed_angles = msm.structure.get_angles(
        path,
        triplets,
        pbc=False,
        use_gpu=False,
    )
    observed_dihedrals = msm.structure.get_dihedral_angles(
        path,
        dihedral_quartets=quartets,
        pbc=False,
        use_gpu=False,
    )

    for expected in (expected_distances_mdtraj, expected_distances_mda):
        np.testing.assert_allclose(
            _values(observed_distances, "nm"),
            expected,
            rtol=0.0,
            atol=external_float32_atol,
        )
    for expected in (expected_angles_mdtraj, expected_angles_mda):
        np.testing.assert_allclose(
            _values(observed_angles, "radians"),
            expected,
            rtol=0.0,
            atol=external_float32_atol,
        )
    for expected in (expected_dihedrals_mdtraj, expected_dihedrals_mda):
        _assert_angles_equivalent(
            _values(observed_dihedrals, "radians"),
            expected,
            external_float32_atol,
        )


def test_pentalanine_trajectory_phi_and_psi_agree_with_mdtraj(
    external_float32_atol,
):
    """Compare backbone dihedrals across four separated trajectory frames."""

    path = systems["pentalanine"]["traj_pentalanine.h5"]
    structure_indices = [0, 1000, 2500, 4999]
    trajectory = md.load(str(path))
    phi_quartets, phi = md.compute_phi(trajectory)
    psi_quartets, psi = md.compute_psi(trajectory)
    quartets = np.concatenate([phi_quartets, psi_quartets])
    expected = np.concatenate(
        [phi[structure_indices], psi[structure_indices]],
        axis=1,
    )

    observed = msm.structure.get_dihedral_angles(
        path,
        dihedral_quartets=quartets,
        structure_indices=structure_indices,
        pbc=False,
        use_gpu=False,
    )

    np.testing.assert_allclose(
        _values(observed, "radians"),
        expected,
        rtol=0.0,
        atol=external_float32_atol,
    )
