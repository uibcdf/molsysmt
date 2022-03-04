"""
Unit and regression test for the view module of the molsysmt package on molsysmt.MolSys.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

def test_view_molsyst_MolSys_with_NLGView_1():

    import nglview as nv

    molsys = msm.demo['T4 lysozyme L99A']['181l.pdb']
    molsys = msm.convert(molsys, to_form='molsysmt.MolSys')
    molsys_2 = nv.show_molsysmt(molsys)
    check = ('nglview.NGLWidget'==msm.get_form(molsys_2))
    check_n_elements = msm.compare(molsys, molsys_2, comparison='n_elements')
    check_n_molecules = msm.compare(molsys, molsys_2, comparison='n_molecules')
    check_n_structures = msm.compare(molsys, molsys_2, comparison='n_structures')
    assert check and check_n_elements and check_n_molecules and check_n_structures

def test_view_molsyst_MolSys_with_NGLView_2():

    molsys = msm.convert(msm.demo['alanine dipeptide']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    view = msm.view(molsys, viewer='NGLView')
    check_comparison = msm.compare(view, molsys, rule='A_eq_B', comparison='info_no_form')
    assert check_comparison

def test_view_molsyst_MolSys_with_NGLView_3():

    molsys = msm.convert(msm.demo['alanine dipeptide']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    view = msm.view(molsys, standardize=True, viewer='NGLView')
    check_comparison = msm.compare(view, molsys, rule='A_eq_B', comparison='info_no_form')
    assert check_comparison

def test_view_molsyst_MolSys_with_NGLView_4():

    molsys_1 = msm.convert(msm.demo['alanine dipeptide']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    molsys_2 = msm.structure.translate(molsys_1, translation='[0.5, 0.0, 0.0] nm')
    view = msm.view([molsys_1, molsys_2], viewer='NGLView')
    molsys_merged = msm.merge([molsys_1, molsys_2])
    check_comparison = msm.compare(view, molsys_merged, rule='A_eq_B', comparison='info_no_form')
    assert check_comparison

def test_view_molsyst_MolSys_with_NGLView_5():

    molsys_1 = msm.convert(msm.demo['alanine dipeptide']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    molsys_2 = msm.structure.translate(molsys_1, translation='[0.5, 0.0, 0.0] nm')
    view = msm.view([molsys_1, molsys_2], concatenate_structures=True, viewer='NGLView')
    molsys_concatenated = msm.concatenate_structures([molsys_1, molsys_2])
    check_comparison = msm.compare(view, molsys_concatenated, rule='A_eq_B', comparison='info_no_form')
    assert check_comparison

