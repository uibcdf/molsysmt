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

    assert [atom["atom_id"] for atom in output.data["topology"]["atoms"]] == [
        "100",
        "102",
    ]
    assert msm.get(output, structure_id=True) == ["50", "10"]
    assert puw.get_value(msm.get(output, time=True), to_unit="ps").tolist() == [
        5.0,
        0.0,
    ]
    coordinates = puw.get_value(msm.get(output, coordinates=True), to_unit="nm")
    assert coordinates.shape == (2, 2, 3)
    np.testing.assert_allclose(
        coordinates,
        puw.get_value(rich_molsys.structures.coordinates, to_unit="nm")[[2, 0]][
            :, [0, 2], :
        ],
    )


def test_molsysdict_extraction_keeps_canonical_atoms_and_requested_structures(
    rich_molsys,
):
    source = msm.convert(rich_molsys, to_form="molsysmt.MolSysDict")

    output = msm.extract(
        source,
        selection=[2, 0],
        structure_indices=[2, 0],
    )

    assert [atom["atom_id"] for atom in output.data["topology"]["atoms"]] == [
        "100",
        "102",
    ]
    assert msm.get(output, structure_id=True) == ["50", "10"]
    assert puw.get_value(msm.get(output, time=True), to_unit="ps").tolist() == [
        5.0,
        0.0,
    ]
    coordinates = puw.get_value(msm.get(output, coordinates=True), to_unit="nm")
    assert coordinates.shape == (2, 2, 3)
    np.testing.assert_allclose(
        coordinates,
        puw.get_value(rich_molsys.structures.coordinates, to_unit="nm")[[2, 0]][
            :, [0, 2], :
        ],
    )


def test_topologydict_extraction_remaps_stable_hierarchy_without_chemistry(rich_molsys):
    source = msm.convert(rich_molsys.topology, to_form="molsysmt.TopologyDict")

    output = msm.extract(source, selection=[3, 2, 0])
    data = output.data

    assert [atom["atom_id"] for atom in data["atoms"]] == ["100", "102", "103"]
    assert [atom["group_index"] for atom in data["atoms"]] == [0, 1, 1]
    assert [group["molecule_index"] for group in data["groups"]] == [0, 1]
    assert [molecule["entity_index"] for molecule in data["molecules"]] == [0, 1]
    assert [atom["chain_index"] for atom in data["atoms"]] == [0, 0, 0]
    assert "bonds" not in data and "components" not in data
    complete = msm.extract(rich_molsys, selection=[3, 2, 0])
    assert complete.chemical_states.get_bonds()[
        ["atom1_index", "atom2_index"]
    ].values.tolist() == [[0, 1], [1, 2]]


def test_mdtraj_trajectory_conversion_keeps_selected_topology_and_coordinates_aligned(
    rich_molsys,
):
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
        puw.get_value(rich_molsys.structures.coordinates, to_unit="nm")[[2, 0]][
            :, [0, 2], :
        ],
    )
