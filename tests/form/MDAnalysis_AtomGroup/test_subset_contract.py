"""Testing subset fidelity for MDAnalysis AtomGroup adapters."""

import numpy as np

import molsysmt as msm
from molsysmt import pyunitwizard as puw


def test_atomgroup_to_universe_does_not_reintroduce_parent_atoms(rich_universe):
    atom_group = rich_universe.atoms[[3, 1, 2]]

    output = msm.convert(atom_group, to_form="MDAnalysis.Universe")

    assert output.atoms.ids.tolist() == [13, 11, 12]
    assert len(output.trajectory) == 3


def test_atomgroup_molsys_subset_keeps_topology_and_coordinates_aligned(
    rich_universe,
):
    atom_group = rich_universe.atoms[[3, 1, 2]]

    output = msm.convert(
        atom_group,
        to_form="molsysmt.MolSys",
        selection=[2, 0],
        structure_indices=[2, 0],
    )

    assert output.topology.atoms["atom_id"].tolist() == ["12", "13"]
    np.testing.assert_allclose(
        puw.get_value(output.structures.coordinates, to_unit="angstrom"),
        rich_universe.trajectory.timeseries(order="fac")[[2, 0]][:, [2, 3]],
    )


def test_atomgroup_extract_applies_atoms_and_structures(rich_universe):
    atom_group = rich_universe.atoms[[3, 1, 2]]

    output = msm.extract(
        atom_group,
        selection=[1, 2],
        structure_indices=[0, 2],
        to_form="MDAnalysis.AtomGroup",
    )

    assert output.ids.tolist() == [11, 12]
    assert len(output.universe.trajectory) == 2
