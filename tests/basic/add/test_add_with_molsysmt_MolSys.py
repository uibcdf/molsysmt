"""
Unit and regression test for the add module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np
import pytest

def test_add_with_molsysmt_MolSys(proline_molsys,valine_molsys,lysine_molsys):
    molsys_A = proline_molsys
    molsys_B = valine_molsys
    molsys_C = lysine_molsys
    n_atoms_A = msm.get(molsys_A, element='system', n_atoms=True)
    n_atoms_B = msm.get(molsys_B, element='system', n_atoms=True)
    n_atoms_C = msm.get(molsys_C, element='system', n_atoms=True)
    msm.add(molsys_A, molsys_B)
    msm.add(molsys_A, molsys_C)
    n_atoms, n_structures = msm.get(molsys_A, element='system', n_atoms=True, n_structures=True)
    assert 'molsysmt.MolSys'==msm.get_form(molsys_A)
    assert n_atoms == n_atoms_A+n_atoms_B+n_atoms_C
    assert n_structures == 1

def test_add_with_molsysmt_MolSys_2(proline_molsys,valine_molsys):
    molsys_A = proline_molsys
    molsys_B = valine_molsys
    n_molecules_before = msm.get(molsys_A, n_molecules=True)
    molsys_new = msm.add(molsys_A, molsys_B, in_place=False)
    # molsys_A should remain unmodified
    assert msm.get(molsys_A, n_molecules=True) == n_molecules_before
    # molsys_new should be the modified version
    assert msm.get(molsys_new, n_molecules=True) == n_molecules_before + 1

