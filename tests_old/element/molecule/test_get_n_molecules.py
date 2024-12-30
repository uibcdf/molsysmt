"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

def test_get_n_molecules_from_molsysmt_MolSys_1():

    molsys = msm.convert(systems['chicken villin HP35']['chicken_villin_HP35_solvated.h5msm'])
    n_molecules1 = msm.element.molecule.get_n_molecules(molsys)
    n_molecules2 = msm.element.molecule.get_n_molecules(molsys, redefine_molecules=True)
    assert n_molecules1 == 1236
    assert n_molecules2 == 1236


