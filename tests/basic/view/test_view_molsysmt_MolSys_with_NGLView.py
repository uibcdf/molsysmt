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

    molsys = msm.convert(systems['alanine dipeptide']['alanine_dipeptide.h5msm'], to_form='molsysmt.MolSys')
    view = msm.view(molsys, viewer='NGLView')
    check_comparison_1 = msm.compare(view, molsys)
    check_comparison_2 = msm.compare(view, molsys, coordinates=True, box=True)
    assert check_comparison_1
    assert check_comparison_2

def test_view_molsyst_MolSys_with_NGLView_3():

    molsys_1 = msm.convert(systems['alanine dipeptide']['alanine_dipeptide.h5msm'], to_form='molsysmt.MolSys')
    molsys_2 = msm.structure.translate(molsys_1, translation='[0.5, 0.0, 0.0] nm')
    molsys_merged = msm.merge([molsys_1, molsys_2], keep_ids=False)
    msm.build.define_new_chain(molsys_merged, selection='all', chain_id=0, chain_name='A')
    view = msm.view(molsys_merged, viewer='NGLView')
    comparison = msm.compare(view, molsys_merged, attribute_type='topological',
            coordinates=True)
    assert comparison

def test_view_molsyst_MolSys_with_NGLView_4():

    molsys_1 = msm.convert(systems['alanine dipeptide']['alanine_dipeptide.h5msm'], to_form='molsysmt.MolSys')
    molsys_2 = msm.structure.translate(molsys_1, translation='[0.5, 0.0, 0.0] nm')
    molsys_concatenated = msm.concatenate_structures([molsys_1, molsys_2])
    view = msm.view(molsys_concatenated, viewer='NGLView')
    comparison = msm.compare(view, molsys_concatenated, attribute_type='topological',
            coordinates=True, box=True)
    assert comparison

