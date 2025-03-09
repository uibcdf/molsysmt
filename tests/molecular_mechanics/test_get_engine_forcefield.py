"""
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np
from openmm import app

def test_get_engine_forcefield_1():

    output = msm.molecular_mechanics.get_engine_forcefield('AMBER14', engine='OpenMM')
    assert output == ['amber14-all.xml']

def test_get_engine_forcefield_2():

    output = msm.molecular_mechanics.get_engine_forcefield('AMBER14', water_model='TIP3P', engine='OpenMM')
    assert output == ['amber14-all.xml', 'amber14/tip3p.xml']

