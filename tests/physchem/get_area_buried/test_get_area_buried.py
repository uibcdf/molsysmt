"""
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np
from openmm import app

# Distance between atoms in space and time

def test_get_area_buried_1():

    molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'], selection='molecule_type=="protein"')

    n_groups = msm.get(molsys, target='system', n_groups=True)
    rose = msm.physchem.get_area_buried(molsys, definition='rose')

    assert len(rose)==n_groups

