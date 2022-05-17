"""
Unit and regression test for the concatenate module of the molsysmt package with molsysmt.MolSys
objects.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

def test_append_structures_with_molsysmt_MolSys():
    molsys_1 = msm.convert(msm.demo['proline dipeptide']['vacuum.msmpk'], to_form='molsysmt.MolSys')
    molsys_2 = msm.structure.translate(molsys_1, translation='[0.1, 0.1, 0.1] nanometers')
    molsys_3 = msm.structure.translate(molsys_1, translation='[0.2, 0.2, 0.2] nanometers')
    n_atoms_1, n_structures_1 = msm.get(molsys_1, element='system', n_atoms=True, n_structures=True)
    n_structures_2 = msm.get(molsys_2, element='system', n_structures=True)
    n_structures_3 = msm.get(molsys_3, element='system', n_structures=True)
    msm.append_structures(molsys_1, [molsys_2, molsys_3])
    n_atoms, n_structures = msm.get(molsys_1, element='system', n_atoms=True, n_structures=True)
    check = ('molsysmt.MolSys'==msm.get_form(molsys_1))
    check_n_atoms = (n_atoms == n_atoms_1)
    check_n_structures = (n_structures == n_structures_1 + n_structures_2 + n_structures_3)
    assert check and check_n_atoms and check_n_structures

