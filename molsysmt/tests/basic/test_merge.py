"""
Unit and regression test for the merge module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np


def test_merge():
    molsys_1 = msm.demo.classes.proline_dipeptide_vacuum(to_form='molsysmt.MolSys')
    molsys_2 = msm.demo.classes.valine_dipeptide_vacuum(to_form='molsysmt.MolSys')
    molsys_3 = msm.demo.classes.lysine_dipeptide_vacuum(to_form='molsysmt.MolSys')
    n_atoms_1 = msm.get(molsys_1, target='system', n_atoms=True)
    n_atoms_2 = msm.get(molsys_2, target='system', n_atoms=True)
    n_atoms_3 = msm.get(molsys_3, target='system', n_atoms=True)
    molsys = msm.merge([molsys_1, molsys_2, molsys_3])
    n_atoms, n_frames = msm.get(molsys, target='system', n_atoms=True, n_frames=True)
    assert (n_atoms == n_atoms_1+n_atoms_2+n_atoms_3) and (n_frames == 1)

