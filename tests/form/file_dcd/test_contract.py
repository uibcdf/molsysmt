"""Testing the contractual structural scope of the file:dcd adapter."""

from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


DCD_PATH = Path(msm.__file__).parent / "data" / "dcd" / "traj_chicken_villin_HP35_solvated.dcd"


def _read_mdtraj_frames(structure_indices, atom_indices):
    mdtraj = pytest.importorskip("mdtraj")
    coordinates = []
    lengths = []
    angles = []
    with mdtraj.formats.DCDTrajectoryFile(str(DCD_PATH), mode="r") as handle:
        for structure_index in structure_indices:
            handle.seek(structure_index)
            xyz, cell_lengths, cell_angles = handle.read(
                n_frames=1,
                atom_indices=atom_indices,
            )
            coordinates.append(xyz[0])
            lengths.append(cell_lengths[0])
            angles.append(cell_angles[0])
    return np.asarray(coordinates), np.asarray(lengths), np.asarray(angles)


def test_file_dcd_reports_structural_dimensions():
    assert msm.get(DCD_PATH, element="system", n_atoms=True) == 4369
    assert msm.get(DCD_PATH, element="system", n_structures=True) == 20


def test_file_dcd_preserves_nonmonotonic_frame_and_atom_subsets():
    structure_indices = [7, 1, 12]
    atom_indices = [4, 1, 9]
    expected_coordinates, expected_lengths, expected_angles = _read_mdtraj_frames(
        structure_indices,
        atom_indices,
    )

    structures = msm.convert(
        DCD_PATH,
        to_form="molsysmt.Structures",
        selection=atom_indices,
        structure_indices=structure_indices,
    )

    np.testing.assert_allclose(
        puw.get_value(structures.coordinates, to_unit="angstrom"),
        expected_coordinates,
        rtol=0.0,
        atol=1.0e-6,
    )
    assert structures.structure_id.tolist() == structure_indices

    observed_lengths, observed_angles = msm.pbc.get_lengths_and_angles_from_box(
        structures.box
    )
    np.testing.assert_allclose(
        puw.get_value(observed_lengths, to_unit="angstrom"),
        expected_lengths,
        rtol=0.0,
        atol=1.0e-5,
    )
    np.testing.assert_allclose(
        puw.get_value(observed_angles, to_unit="degree"),
        expected_angles,
        rtol=0.0,
        atol=3.0e-5,
    )


def test_file_dcd_builds_an_index_only_topology_for_standalone_use():
    output = msm.convert(
        DCD_PATH,
        to_form="molsysmt.MolSys",
        selection=[2, 8],
        structure_indices=[3, 0],
    )

    assert output.topology.n_atoms == 2
    assert output.topology.atoms.index.tolist() == [0, 1]
    assert output.topology.atoms["atom_id"].isna().all()
    assert output.structures.coordinates.shape == (2, 2, 3)
    assert output.structures.structure_id.tolist() == [3, 0]


def test_file_dcd_does_not_claim_unavailable_time():
    assert msm.has_attribute(DCD_PATH, "time") is False
    assert msm.get(DCD_PATH, element="system", time=True) is None
