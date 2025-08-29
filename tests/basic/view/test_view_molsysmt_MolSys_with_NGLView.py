"""
Unit and regression test for the view module of the molsysmt package on molsysmt.MolSys.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

def test_view_molsyst_MolSys_with_NLGView_1():

    import nglview as nv

    molsys = systems['T4 lysozyme L99A']['181l.pdb']
    molsys = msm.convert(molsys, to_form='molsysmt.MolSys')
    molsys_2 = nv.show_molsysmt(molsys)
    check = ('nglview.NGLWidget'==msm.get_form(molsys_2))
    n_molecules, n_structures = msm.get(molsys, element='system', n_molecules=True, n_structures=True)
    n_molecules_2, n_structures_2 = msm.get(molsys_2, element='system', n_molecules=True, n_structures=True)
    check_n_molecules = (n_molecules==n_molecules_2)
    check_n_structures = (n_structures==n_structures_2)
    assert check and check_n_molecules and check_n_structures

def test_view_molsyst_MolSys_with_NGLView_2():

    aux_dict = {'atom_index': True,
                'atom_name': True,
                'atom_id': True,
                'atom_type': True,
                'group_index': True,
                'group_name': True,
                'group_id': True,
                'group_type': True,
                'component_index': True,
                'component_type': True,
                'chain_index': True,
                'chain_name': True,
                'chain_id': False,
                'chain_type': True,
                'molecule_index': True,
                'molecule_type': True,
                'bonded_atom_pairs': True,
                'n_atoms': True,
                'n_groups': True,
                'n_components': True,
                'n_chains': True,
                'n_molecules': True,
                'n_bonds': True}

    molsys = msm.convert(systems['alanine dipeptide']['alanine_dipeptide.h5msm'], to_form='molsysmt.MolSys')
    view = msm.view(molsys, viewer='NGLView')
    check_comparison_1 = msm.compare(view, molsys, output_type='dictionary')
    check_comparison_2 = msm.compare(view, molsys, coordinates=True, box=True)
    assert check_comparison_1 == aux_dict
    assert check_comparison_2

def test_view_molsyst_MolSys_with_NGLView_3():

    aux_dict = {'atom_index': True,
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
                'n_inner_bonds': True,
                'coordinates': True}

    molsys_1 = msm.convert(systems['alanine dipeptide']['alanine_dipeptide.h5msm'], to_form='molsysmt.MolSys')
    molsys_2 = msm.structure.translate(molsys_1, translation='[0.5, 0.0, 0.0] nm')
    molsys_merged = msm.merge([molsys_1, molsys_2], keep_ids=False)
    msm.build.define_new_chain(molsys_merged, selection='all', chain_id=0, chain_name='A')
    view = msm.view(molsys_merged, viewer='NGLView')
    comparison = msm.compare(view, molsys_merged, attribute_type='topological', coordinates=True,
                             output_type='dictionary')
    assert comparison == aux_dict

def test_view_molsyst_MolSys_with_NGLView_4():

    aux_dict = {'atom_index': True,
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
                'n_inner_bonds': True,
                'coordinates': True,
                'box': True}

    molsys_1 = msm.convert(systems['alanine dipeptide']['alanine_dipeptide.h5msm'], to_form='molsysmt.MolSys')
    molsys_2 = msm.structure.translate(molsys_1, translation='[0.5, 0.0, 0.0] nm')
    molsys_concatenated = msm.concatenate_structures([molsys_1, molsys_2])
    view = msm.view(molsys_concatenated, viewer='NGLView')
    comparison = msm.compare(view, molsys_concatenated, attribute_type='topological',
            coordinates=True, box=True, output_type='dictionary')
    assert comparison == aux_dict

def test_view_molsyst_MolSys_with_NGLView_5():

    aux_dict = {'atom_index': True,
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
                'n_inner_bonds': True,
                'coordinates': True,
                'box': True}

    molsys = msm.convert(systems['alanine dipeptide']['alanine_dipeptide.h5msm'], to_form='molsysmt.MolSys')
    view = msm.view(molsys, viewer='NGLView', standard=True)
    comparison = msm.compare(view, molsys, attribute_type='topological', coordinates=True, box=True,
                             output_type='dictionary')
    assert comparison == aux_dict

def test_view_molsyst_MolSys_with_NGLView_6():

    molsys = msm.systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm']
    view = msm.view(molsys, viewer='NGLView', standard=True)
    comparison = msm.compare(view, molsys, attribute_type='topological', coordinates=True, box=True,
                             component_name=False, molecule_name=False, entity_name=False, atom_type=False)
    assert comparison

