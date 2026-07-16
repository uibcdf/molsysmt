"""Curated scientific agreement tests for the Trp-cage NMR ensemble."""

import warnings

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import Structures


md = pytest.importorskip("mdtraj")
mda = pytest.importorskip("MDAnalysis")
from MDAnalysis.analysis.rms import rmsd
from MDAnalysis.lib.distances import calc_bonds, calc_dihedrals


CA_INDICES = np.array(
    [1, 17, 36, 57, 76, 93, 117, 136, 158, 170, 177, 184, 198, 209, 220, 227, 251, 265, 279, 293],
    dtype=np.int64,
)
FRAME_INDICES = np.array([0, 9, 19, 28, 37], dtype=np.int64)
PHI_QUARTETS = np.array(
    [[2, 16, 17, 18], [77, 92, 93, 94], [266, 278, 279, 280]],
    dtype=np.int64,
)


@pytest.fixture(scope="module")
def trp_cage_readers(trp_cage_pdb_path):
    """Load the same versioned PDB ensemble with three independent readers."""

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="Unlikely unit cell vectors")
        mdtraj_trajectory = md.load(trp_cage_pdb_path)

    mdanalysis_universe = mda.Universe(trp_cage_pdb_path)
    mdanalysis_coordinates = np.stack(
        [
            mdanalysis_universe.trajectory[index].positions.copy() / 10.0
            for index in range(len(mdanalysis_universe.trajectory))
        ]
    )
    molsysmt_coordinates = msm.get(
        trp_cage_pdb_path,
        element="atom",
        coordinates=True,
    )
    molsysmt_coordinates = msm.pyunitwizard.get_value(
        molsysmt_coordinates,
        to_unit="nm",
    )

    return mdtraj_trajectory, mdanalysis_universe, mdanalysis_coordinates, molsysmt_coordinates


def test_trp_cage_reader_identity_and_ca_mapping(trp_cage_readers):
    """Validate the ensemble identity before comparing scientific quantities."""

    trajectory, universe, _, molsysmt_coordinates = trp_cage_readers

    assert trajectory.n_frames == 38
    assert trajectory.n_atoms == 304
    assert trajectory.n_residues == 20
    assert len(universe.trajectory) == 38
    assert universe.atoms.n_atoms == 304
    assert universe.residues.n_residues == 20
    assert molsysmt_coordinates.shape == (38, 304, 3)
    np.testing.assert_array_equal(trajectory.topology.select("name CA"), CA_INDICES)
    np.testing.assert_array_equal(universe.select_atoms("name CA").indices, CA_INDICES)


def test_trp_cage_ca_coordinates_agree_across_readers(
    trp_cage_readers,
    external_float32_atol,
):
    """Compare C-alpha coordinates in nanometers for all 38 NMR models."""

    trajectory, _, mdanalysis_coordinates, molsysmt_coordinates = trp_cage_readers

    np.testing.assert_allclose(
        molsysmt_coordinates[:, CA_INDICES, :],
        trajectory.xyz[:, CA_INDICES, :],
        rtol=0.0,
        atol=external_float32_atol,
    )
    np.testing.assert_allclose(
        molsysmt_coordinates[:, CA_INDICES, :],
        mdanalysis_coordinates[:, CA_INDICES, :],
        rtol=0.0,
        atol=external_float32_atol,
    )


def test_trp_cage_ca_distances_agree_with_both_oracles(
    trp_cage_readers,
    external_float32_atol,
):
    """Compare adjacent C-alpha distances across representative NMR models."""

    trajectory, _, mdanalysis_coordinates, molsysmt_coordinates = trp_cage_readers
    pairs = np.column_stack([CA_INDICES[:-1], CA_INDICES[1:]])
    expected_mdtraj = md.compute_distances(
        trajectory[FRAME_INDICES],
        pairs,
        periodic=False,
        opt=False,
    )
    expected_mdanalysis = np.stack(
        [
            calc_bonds(frame[pairs[:, 0]], frame[pairs[:, 1]])
            for frame in mdanalysis_coordinates[FRAME_INDICES]
        ]
    )
    structures = Structures(
        coordinates=molsysmt_coordinates[FRAME_INDICES] * msm.pyunitwizard.unit("nm")
    )
    observed = msm.structure.get_distances(
        structures,
        selection=pairs,
        pairs=True,
        pbc=False,
        heavy_mode="off",
        use_gpu=False,
    )
    observed = msm.pyunitwizard.get_value(observed, to_unit="nm")

    np.testing.assert_allclose(observed, expected_mdtraj, rtol=0.0, atol=external_float32_atol)
    np.testing.assert_allclose(observed, expected_mdanalysis, rtol=0.0, atol=external_float32_atol)


def test_trp_cage_phi_dihedrals_agree_with_both_oracles(
    trp_cage_readers,
    external_float32_atol,
):
    """Compare signed backbone phi angles across representative NMR models."""

    trajectory, _, mdanalysis_coordinates, molsysmt_coordinates = trp_cage_readers
    expected_mdtraj = md.compute_dihedrals(
        trajectory[FRAME_INDICES],
        PHI_QUARTETS,
        periodic=False,
        opt=False,
    )
    expected_mdanalysis = np.stack(
        [
            calc_dihedrals(
                frame[PHI_QUARTETS[:, 0]],
                frame[PHI_QUARTETS[:, 1]],
                frame[PHI_QUARTETS[:, 2]],
                frame[PHI_QUARTETS[:, 3]],
            )
            for frame in mdanalysis_coordinates[FRAME_INDICES]
        ]
    )
    structures = Structures(
        coordinates=molsysmt_coordinates[FRAME_INDICES] * msm.pyunitwizard.unit("nm")
    )
    observed = msm.structure.get_dihedral_angles(
        structures,
        dihedral_quartets=PHI_QUARTETS,
        pbc=False,
        use_gpu=False,
    )
    observed = msm.pyunitwizard.get_value(observed, to_unit="radians")

    np.testing.assert_allclose(observed, expected_mdtraj, rtol=0.0, atol=external_float32_atol)
    np.testing.assert_allclose(observed, expected_mdanalysis, rtol=0.0, atol=external_float32_atol)


def test_trp_cage_ca_least_rmsd_agrees_with_both_oracles(
    trp_cage_readers,
    external_float32_atol,
):
    """Compare least-RMSD for all NMR models against model one."""

    trajectory, _, mdanalysis_coordinates, molsysmt_coordinates = trp_cage_readers
    expected_mdtraj = md.rmsd(
        md.Trajectory(trajectory.xyz[:, CA_INDICES, :].copy(), topology=None),
        md.Trajectory(trajectory.xyz[[0]][:, CA_INDICES, :].copy(), topology=None),
        frame=0,
        parallel=False,
    )
    ca_coordinates_mda = mdanalysis_coordinates[:, CA_INDICES, :]
    expected_mdanalysis = np.array(
        [
            rmsd(frame, ca_coordinates_mda[0], center=True, superposition=True)
            for frame in ca_coordinates_mda
        ]
    )
    structures = Structures(
        coordinates=molsysmt_coordinates[:, CA_INDICES, :] * msm.pyunitwizard.unit("nm")
    )
    observed = msm.structure.get_least_rmsd(
        structures,
        selection="all",
        reference_structure_index=0,
        use_gpu=False,
    )
    observed = msm.pyunitwizard.get_value(observed, to_unit="nm")

    np.testing.assert_allclose(observed, expected_mdtraj, rtol=0.0, atol=external_float32_atol)
    np.testing.assert_allclose(observed, expected_mdanalysis, rtol=0.0, atol=external_float32_atol)
