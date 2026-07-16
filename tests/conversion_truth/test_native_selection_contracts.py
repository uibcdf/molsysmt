import numpy as np

import molsysmt as msm
from molsysmt import pyunitwizard as puw


def test_molsysdict_conversion_applies_atom_and_structure_selection(rich_molsys):
    output = msm.convert(
        rich_molsys,
        to_form="molsysmt.MolSysDict",
        selection=[2, 0],
        structure_indices=[2, 0],
    )

    assert [atom["atom_id"] for atom in output.data["topology"]["atoms"]] == ["100", "102"]
    assert output.data["structures"]["structure_id"] == [50, 10]
    assert output.data["structures"]["time"] == [5.0, 0.0]
    coordinates = np.asarray(output.data["structures"]["coordinates"])
    assert coordinates.shape == (2, 2, 3)
    np.testing.assert_allclose(
        coordinates,
        puw.get_value(rich_molsys.structures.coordinates, to_unit="nm")[[2, 0]][:, [0, 2], :],
    )


def test_mdtraj_trajectory_conversion_keeps_selected_topology_and_coordinates_aligned(rich_molsys):
    mdtraj = __import__("pytest").importorskip("mdtraj")

    output = msm.convert(
        rich_molsys,
        to_form="mdtraj.Trajectory",
        selection=[2, 0],
        structure_indices=[2, 0],
    )

    assert isinstance(output, mdtraj.Trajectory)
    assert output.n_atoms == 2
    assert output.n_frames == 2
    assert [atom.serial for atom in output.topology.atoms] == ["100", "102"]
    np.testing.assert_allclose(
        output.xyz,
        puw.get_value(rich_molsys.structures.coordinates, to_unit="nm")[[2, 0]][:, [0, 2], :],
    )
