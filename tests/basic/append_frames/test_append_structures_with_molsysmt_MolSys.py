"""
Unit and regression test for the concatenate module of the molsysmt package with molsysmt.MolSys
objects.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

def test_append_structures_with_molsysmt_MolSys_1():
    molsys_A = msm.convert(systems['proline dipeptide']['proline_dipeptide.h5msm'], to_form='molsysmt.MolSys')
    molsys_B = msm.structure.translate(molsys_A, translation='[0.1, 0.1, 0.1] nanometers')
    molsys_C = msm.structure.translate(molsys_A, translation='[0.2, 0.2, 0.2] nanometers')
    n_atoms_A, n_structures_A = msm.get(molsys_A, element='system', n_atoms=True, n_structures=True)
    n_structures_B = msm.get(molsys_B, element='system', n_structures=True)
    n_structures_C = msm.get(molsys_C, element='system', n_structures=True)
    msm.append_structures(molsys_A, molsys_B)
    msm.append_structures(molsys_A, molsys_C)
    n_atoms, n_structures = msm.get(molsys_A, element='system', n_atoms=True, n_structures=True)
    assert 'molsysmt.MolSys'==msm.get_form(molsys_A)
    assert n_atoms == n_atoms_A
    assert n_structures == n_structures_A + n_structures_B + n_structures_C

def test_append_structures_with_molsysmt_MolSys_2():
    molsys_A = msm.convert(systems['proline dipeptide']['proline_dipeptide.h5msm'], to_form='molsysmt.MolSys')
    molsys_B = msm.structure.translate(molsys_A, translation='[0.1, 0.1, 0.1] nanometers')
    molsys_C = msm.append_structures(molsys_A, molsys_B, in_place=False)
    n_atoms_A, n_structures_A = msm.get(molsys_A, element='system', n_atoms=True, n_structures=True)
    n_atoms_B, n_structures_B = msm.get(molsys_B, element='system', n_atoms=True, n_structures=True)
    n_atoms_C, n_structures_C = msm.get(molsys_C, element='system', n_atoms=True, n_structures=True)
    assert 'molsysmt.MolSys'==msm.get_form(molsys_A)
    assert n_atoms_C == n_atoms_A
    assert n_structures_C == n_structures_A + n_structures_B

