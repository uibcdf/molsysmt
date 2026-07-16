import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.fixture
def rich_molsys():
    """Build a small system exercising topology, hierarchy, and trajectory metadata."""

    builder = msm.MolSysBuilder()
    atom_indices = [
        builder.add_atom(atom_id=atom_id, atom_name=name, atom_type=atom_type)
        for atom_id, name, atom_type in [
            ("100", "N", "N"),
            ("101", "CA", "C"),
            ("102", "C", "C"),
            ("103", "O", "O"),
        ]
    ]
    group_0 = builder.add_group(atom_indices[:2], group_id="10", group_name="ALA", group_type="amino acid")
    group_1 = builder.add_group(atom_indices[2:], group_id="11", group_name="GLY", group_type="amino acid")
    builder.add_bond(0, 1, bond_order=1)
    builder.add_bond(0, 2)
    builder.add_bond(2, 3, bond_type="covalent")
    builder.add_chain([group_0, group_1], chain_id="A", chain_name="peptide")
    molecule_0 = builder.add_molecule([group_0], molecule_id="20", molecule_name="alanine", molecule_type="peptide")
    molecule_1 = builder.add_molecule([group_1], molecule_id="21", molecule_name="glycine", molecule_type="peptide")
    builder.add_entity([molecule_0], entity_id="30", entity_name="alanine", entity_type="peptide")
    builder.add_entity([molecule_1], entity_id="31", entity_name="glycine", entity_type="peptide")

    coordinates = np.array(
        [
            [[0.012345678, 0.0, 0.0], [0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]],
            [[1.0, 1.1, 1.2], [1.3, 1.4, 1.5], [1.6, 1.7, 1.8], [1.9, 2.0, 2.1]],
            [[2.2, 2.3, 2.4], [2.5, 2.6, 2.7], [2.8, 2.9, 3.0], [3.1, 3.2, 3.3]],
        ]
    )
    box = np.array(
        [
            [[3.0, 0.0, 0.0], [0.2, 3.1, 0.0], [0.1, 0.3, 3.2]],
            [[3.3, 0.0, 0.0], [0.2, 3.4, 0.0], [0.1, 0.3, 3.5]],
            [[3.6, 0.0, 0.0], [0.2, 3.7, 0.0], [0.1, 0.3, 3.8]],
        ]
    )
    builder.set_coordinates(puw.quantity(coordinates, "nm"))
    builder.set_box(puw.quantity(box, "nm"))
    builder.set_time(puw.quantity(np.array([0.0, 2.0, 5.0]), "ps"))
    builder.set_structure_id([10, 20, 50])

    return builder.build()
