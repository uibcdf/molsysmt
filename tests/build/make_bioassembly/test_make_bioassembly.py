"""
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

# Distance between atoms in space and time


def test_make_bioassembly_molsysmt_MolSys_1():
    molsys = msm.convert('3U71')
    n_atoms = msm.get(molsys, target='system', n_atoms=True)
    molsys_2 = msm.build.make_bioassembly(molsys)
    molsys_3 = msm.build.make_bioassembly(molsys, bioassembly='1')
    n_atoms_2 = msm.get(molsys_2, target='system', n_atoms=True)
    n_atoms_3 = msm.get(molsys_3, target='system', n_atoms=True)
    assert n_atoms==755
    assert n_atoms_2==1510
    assert n_atoms_3==1510


