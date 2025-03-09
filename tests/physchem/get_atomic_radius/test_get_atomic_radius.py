"""
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np


def test_get_atom_radius_1():

    molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'], selection='molecule_type=="protein"')

    n_atoms = msm.get(molsys, target='system', n_atoms=True)
    vdw = msm.physchem.get_atomic_radius(molsys, definition='vdw')

    assert len(vdw)==n_atoms

