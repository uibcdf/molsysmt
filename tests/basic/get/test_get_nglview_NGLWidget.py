"""
Unit and regression test for the get module of the molsysmt package on xtc file systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np


def test_get_nglview_NGLWidget_1():
    molsys = msm.convert([msm.systems['nglview']['md_1u19.gro'], msm.systems['nglview']['md_1u19.xtc']],
                         to_form='molsysmt.MolSys')
    view = msm.convert(molsys, to_form='nglview.NGLWidget')
    check_comparison = msm.compare(molsys, view, attribute_type='topological', rule='equal', output_type='dictionary')

    known_comparison = {'atom_index': True,
                        'atom_name': True,
                        'atom_id': True,
                        'atom_type': True,
                        'group_index': True,
                        'group_name': True,
                        'group_id': True,
                        'group_type': True,
                        'component_index': True,
                        'component_name': True,
                        'component_id': True,
                        'component_type': True,
                        'chain_index': True,
                        'chain_name': True,
                        'chain_id': False,
                        'chain_type': True,
                        'molecule_index': True,
                        'molecule_name': True,
                        'molecule_id': True,
                        'molecule_type': True,
                        'entity_index': True,
                        'entity_name': True,
                        'entity_id': True,
                        'entity_type': True,
                        'bond_index': True,
                        'bond_type': True,
                        'bond_order': True,
                        'bonded_atom_pairs': True,
                        'inner_bonded_atom_pairs': True,
                        'inner_bond_index': True,
                        'n_atoms': True,
                        'n_groups': True,
                        'n_components': True,
                        'n_chains': True,
                        'n_molecules': True,
                        'n_entities': True,
                        'n_bonds': True,
                        'n_inner_bonds': True}

    assert check_comparison==known_comparison


def test_get_nglview_NGLWidget_preserves_chain_and_entity_semantics_for_t4():
    molsys = msm.systems['T4 lysozyme L99A']['181l.h5msm']
    view = msm.convert(molsys, to_form='nglview.NGLWidget')

    assert msm.get(view, n_chains=True) == msm.get(molsys, n_chains=True)
    assert msm.get(view, element='chain', chain_type=True) == msm.get(molsys, element='chain', chain_type=True)
    assert msm.get(view, element='molecule', molecule_type=True) == msm.get(molsys, element='molecule', molecule_type=True)
    assert msm.get(view, element='entity', entity_type=True) == msm.get(molsys, element='entity', entity_type=True)
