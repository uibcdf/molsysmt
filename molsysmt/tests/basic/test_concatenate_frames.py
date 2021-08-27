"""
Unit and regression test for the merge module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np


def test_merge():
    molsys_1 = msm.demo.classes.proline_dipeptide_vacuum(to_form='molsysmt.MolSys')
    molsys_2 = msm.structure.translate(molsys_1, translation='[0.1, 0.1, 0.1] nanometers')
    molsys_3 = msm.structure.translate(molsys_1, translation='[0.2, 0.2, 0.2] nanometers')
    n_atoms_1, n_frames_1 = msm.get(molsys_1, target='system', n_atoms=True, n_frames=True)
    n_frames_2 = msm.get(molsys_2, target='system', n_frames=True)
    n_frames_3 = msm.get(molsys_3, target='system', n_frames=True)
    molsys = msm.concatenate_frames([molsys_1, molsys_2, molsys_3])
    n_atoms, n_frames = msm.get(molsys, target='system', n_atoms=True, n_frames=True)
    assert (n_atoms == n_atoms_1) and (n_frames == n_frames_1 + n_frames_2 + n_frames_3)

