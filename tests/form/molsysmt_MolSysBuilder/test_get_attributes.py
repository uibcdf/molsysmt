import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt.form.molsysmt_MolSysBuilder import get_structural_attributes as structural_aux
from molsysmt.form.molsysmt_MolSysBuilder import get_topological_attributes as topological_aux


def test_get_declared_topological_attributes(molsys_builder_partial, molsys_builder_complete):

    assert topological_aux.get_n_atoms_from_system(molsys_builder_partial) == 3
    assert topological_aux.get_n_groups_from_system(molsys_builder_partial) == 1
    assert topological_aux.get_n_bonds_from_system(molsys_builder_partial) == 1
    assert topological_aux.get_n_molecules_from_system(molsys_builder_partial) == 0
    assert topological_aux.get_atom_name_from_atom(molsys_builder_partial) == ["Ar", "Ar", "Ar"]
    assert topological_aux.get_group_index_from_atom(molsys_builder_partial) == [0, 0, None]
    assert topological_aux.get_group_name_from_group(molsys_builder_partial) == ["GAS"]
    assert topological_aux.get_bonded_atom_pairs_from_system(molsys_builder_partial) == [[0, 1]]

    assert topological_aux.get_chain_name_from_chain(molsys_builder_complete) == ["A"]
    assert topological_aux.get_molecule_name_from_molecule(molsys_builder_complete) == ["protein 0", "water"]
    assert topological_aux.get_entity_name_from_entity(molsys_builder_complete) == ["protein 0", "water"]


def test_get_declared_structural_attributes(molsys_builder_complete):

    assert structural_aux.get_n_atoms_from_system(molsys_builder_complete) == 3
    assert structural_aux.get_n_structures_from_system(molsys_builder_complete) == 1
    assert structural_aux.get_structure_id_from_system(molsys_builder_complete) == [0]
    assert puw.get_value(structural_aux.get_time_from_system(molsys_builder_complete), to_unit="ps").tolist() == [0.0]
    assert puw.get_value(structural_aux.get_box_from_system(molsys_builder_complete), to_unit="nm").shape == (1, 3, 3)
    assert np.allclose(
        puw.get_value(structural_aux.get_coordinates_from_system(molsys_builder_complete), to_unit="nm"),
        np.array([[[0.0, 0.0, 0.0], [0.1, 0.0, 0.0], [0.2, 0.0, 0.0]]]),
    )
