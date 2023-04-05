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
    n_molecules, n_structures = msm.get(molsys, element='system', n_molecules=True, n_structures=True)
    n_molecules_2, n_structures_2 = msm.get(molsys_2, element='system', n_molecules=True, n_structures=True)
    check_n_molecules = (n_molecules==n_molecules_2)
    check_n_structures = (n_structures==n_structures_2)
    assert check and check_n_molecules and check_n_structures

def test_view_molsyst_MolSys_with_NGLView_2():

    molsys = msm.convert(msm.demo['alanine dipeptide']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    view = msm.view(molsys, viewer='NGLView')
    check_comparison_1 = msm.compare(view, molsys, rule='equal')
    check_comparison_2 = msm.compare(view, molsys, rule='equal', coordinates=True, box=True)
    assert check_comparison_1
    assert check_comparison_2

#def test_view_molsyst_MolSys_with_NGLView_3():
#
#    molsys = msm.convert(msm.demo['alanine dipeptide']['vacuum.msmpk'], to_form='molsysmt.MolSys')
#    view = msm.view(molsys, viewer='NGLView')
#    check_comparison_1 = msm.compare(view, molsys, rule='equal')
#    check_comparison_2 = msm.compare(view, molsys, rule='equal', coordinates=True, box=True)
#    assert check_comparison_1
#    assert check_comparison_2

def test_view_molsyst_MolSys_with_NGLView_4():

    molsys_1 = msm.convert(msm.demo['alanine dipeptide']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    molsys_2 = msm.structure.translate(molsys_1, translation='[0.5, 0.0, 0.0] nm')
    molsys_merged = msm.merge([molsys_1, molsys_2])
    view = msm.view(molsys_merged, viewer='NGLView')
    comparison = msm.compare(view, molsys_merged, rule='equal', attributes_type='topological',
            coordinates=True, box=True, output_type='dictionary')
    _ = comparison.pop('atom_id')
    check_comparison = np.all(list(comparison.values()))
    assert check_comparison

def test_view_molsyst_MolSys_with_NGLView_5():

    molsys_1 = msm.convert(msm.demo['alanine dipeptide']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    molsys_2 = msm.structure.translate(molsys_1, translation='[0.5, 0.0, 0.0] nm')
    molsys_concatenated = msm.concatenate_structures([molsys_1, molsys_2])
    view = msm.view(molsys_concatenated, viewer='NGLView')
    comparison = msm.compare(view, molsys_concatenated, rule='equal', attributes_type='topological',
            coordinates=True, box=True, output_type='dictionary')
    _ = comparison.pop('atom_id')
    check_comparison = np.all(list(comparison.values()))
    assert check_comparison

