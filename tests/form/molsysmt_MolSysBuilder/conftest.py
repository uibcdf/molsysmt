import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.fixture
def molsys_builder_partial():

    builder = msm.MolSysBuilder()
    atom_indices = [builder.add_atom(atom_name=name) for name in ["Ar", "Ar", "Ar"]]
    builder.add_group(atom_indices[:2], group_name="GAS")
    builder.add_bond(atom_indices[0], atom_indices[1])

    return builder


@pytest.fixture
def molsys_builder_complete():

    builder = msm.MolSysBuilder()
    atom_indices = [builder.add_atom(atom_name=name) for name in ["N", "CA", "O"]]
    group_index_0 = builder.add_group(atom_indices[:2], group_name="ALA")
    group_index_1 = builder.add_group(atom_indices[2:], group_name="HOH")
    builder.add_bond(atom_indices[0], atom_indices[1])
    builder.add_chain([group_index_0, group_index_1], chain_id="A", chain_name="A", chain_type="mixed")
    molecule_index_0 = builder.add_molecule([group_index_0], molecule_id="10", molecule_name="protein 0", molecule_type="protein")
    molecule_index_1 = builder.add_molecule([group_index_1], molecule_id="11", molecule_name="water", molecule_type="water")
    builder.add_entity([molecule_index_0], entity_id="20", entity_name="protein 0", entity_type="protein")
    builder.add_entity([molecule_index_1], entity_id="21", entity_name="water", entity_type="water")
    builder.set_coordinates(
        puw.quantity(
            np.array(
                [
                    [0.0, 0.0, 0.0],
                    [0.1, 0.0, 0.0],
                    [0.2, 0.0, 0.0],
                ]
            ),
            "nm",
        )
    )
    builder.set_box(puw.quantity(np.eye(3)[np.newaxis, :, :], "nm"))
    builder.set_time(puw.quantity(np.array([0.0]), "ps"))
    builder.set_structure_id([0])

    return builder
