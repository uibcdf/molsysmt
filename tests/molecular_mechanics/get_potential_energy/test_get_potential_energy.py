"""
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np

def test_get_non_bonded_potential_energy_1():

    import molsysmt as msm

    molecular_system = msm.convert(msm.systems['Barnase-Barstar']['barnase_barstar.h5msm'])

    U = msm.molecular_mechanics.get_potential_energy(molecular_system)

    assert puw.are_close(U, '-24849.14865698867 kilojoule/mole')

def test_get_non_bonded_potential_energy_2():

    import molsysmt as msm

    molecular_system = msm.convert(msm.systems['Barnase-Barstar']['barnase_barstar.h5msm'])

    U_dict = msm.molecular_mechanics.get_potential_energy(molecular_system, selection='molecule_name=="BARSTAR"', decomposition=True)

    assert list(U_dict.keys())==['HarmonicBondForce', 'NonbondedForce', 'PeriodicTorsionForce', 'CMMotionRemover', 'HarmonicAngleForce']
