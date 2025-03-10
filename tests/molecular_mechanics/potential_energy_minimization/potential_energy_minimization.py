"""
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np

def test_potential_energy_minimization_1():

    molsys = msm.convert('1VII')
    molsys = msm.basic.remove(molsys, selection='atom_type=="H"')
    molsys = msm.build.add_missing_hydrogens(molsys, pH=7.4)

    U1 = msm.molecular_mechanics.get_potential_energy(molsys)
    molsys = msm.molecular_mechanics.potential_energy_minimization(molsys)
    U2 = msm.molecular_mechanics.get_potential_energy(molsys)

    assert U1>U2

