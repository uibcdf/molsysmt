"""
Unit and regression test for the view module of the molsysmt package on molsysmt.MolSys.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

def test_view_1():

    import nglview as nv

    molsys = msm.demo.classes.T4_Lysozyme_L99A_in_pdbid_181l(to_form='molsysmt.MolSys')
    molsys_2 = nv.show_molsysmt(molsys)
    check_form = ('nglview.NGLWidget'==msm.get_form(molsys_2))
    check_n_elements = msm.compare(molsys, molsys_2, comparison='n_elements')
    check_n_molecules = msm.compare(molsys, molsys_2, comparison='n_molecules')
    check_n_frames = msm.compare(molsys, molsys_2, comparison='n_frames')
    assert check_form and check_n_elements and check_n_molecules and check_n_frames


