"""
Unit and regression test for the view module of the molsysmt package on molsysmt.MolSys.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.systems import tests as tests_systems
import numpy as np

def test_view_molsyst_MolSys_with_NLGView_1():

    import nglview as nv

    molsys = tests_systems['T4 lysozyme L99A']['181l.pdb']
    molsys = msm.convert(molsys, to_form='molsysmt.MolSys')
    molsys_2 = nv.show_molsysmt(molsys)
    check = ('nglview.NGLWidget'==msm.get_form(molsys_2))
    n_molecules, n_structures = msm.get(molsys, element='system', n_molecules=True, n_structures=True)
    n_molecules_2, n_structures_2 = msm.get(molsys_2, element='system', n_molecules=True, n_structures=True)
    check_n_molecules = (n_molecules==n_molecules_2)
    check_n_structures = (n_structures==n_structures_2)
    assert check and check_n_molecules and check_n_structures

def test_view_molsyst_MolSys_with_NGLView_2():

    molsys = msm.convert(tests_systems['alanine dipeptide']['alanine_dipeptide.msmpk'], to_form='molsysmt.MolSys')
    view = msm.view(molsys, viewer='NGLView')
    check_comparison_1 = msm.compare(view, molsys)
    check_comparison_2 = msm.compare(view, molsys, coordinates=True, box=True)
    assert check_comparison_1
    assert check_comparison_2

def test_view_molsyst_MolSys_with_NGLView_3():

    molsys_1 = msm.convert(tests_systems['alanine dipeptide']['alanine_dipeptide.msmpk'], to_form='molsysmt.MolSys')
    molsys_2 = msm.structure.translate(molsys_1, translation='[0.5, 0.0, 0.0] nm')
    molsys_merged = msm.merge([molsys_1, molsys_2])
    view = msm.view(molsys_merged, viewer='NGLView')
    comparison = msm.compare(view, molsys_merged, attributes_type='topological',
            coordinates=True, box=True, atom_id=False, component_name=False, component_id=False,
            bond_index=False, inner_bond_index=False)
    assert comparison

def test_view_molsyst_MolSys_with_NGLView_4():

    molsys_1 = msm.convert(tests_systems['alanine dipeptide']['alanine_dipeptide.msmpk'], to_form='molsysmt.MolSys')
    molsys_2 = msm.structure.translate(molsys_1, translation='[0.5, 0.0, 0.0] nm')
    molsys_concatenated = msm.concatenate_structures([molsys_1, molsys_2])
    view = msm.view(molsys_concatenated, viewer='NGLView')
    comparison = msm.compare(view, molsys_concatenated, attributes_type='topological',
            coordinates=True, box=True, entity_name=False, entity_id=False,
            bond_index=False, inner_bond_index=False)
    assert comparison

