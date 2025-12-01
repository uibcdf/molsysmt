"""
Unit and regression test for the merge module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

def test_merge_molsysmt_MolSys_1(proline_molsys, valine_molsys, lysine_molsys):
    molsys_1 = proline_molsys
    molsys_2 = valine_molsys
    molsys_3 = lysine_molsys
    n_atoms_1 = msm.get(molsys_1, element='system', n_atoms=True)
    n_atoms_2 = msm.get(molsys_2, element='system', n_atoms=True)
    n_atoms_3 = msm.get(molsys_3, element='system', n_atoms=True)
    molsys = msm.merge([molsys_1, molsys_2, molsys_3])
    n_atoms, n_structures = msm.get(molsys, element='system', n_atoms=True, n_structures=True)
    check = ('molsysmt.MolSys'==msm.get_form(molsys))
    check_n_atoms = (n_atoms == n_atoms_1+n_atoms_2+n_atoms_3)
    check_n_structures = (n_structures == 1)
    assert check and check_n_atoms and check_n_structures

