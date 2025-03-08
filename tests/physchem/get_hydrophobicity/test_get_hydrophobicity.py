"""
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np
from openmm import app

# Distance between atoms in space and time

def test_get_hydrophobicity_1():

    molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'], selection='molecule_type=="protein"')

    n_groups = msm.get(molsys, target='system', n_groups=True)
    eisenberg = msm.physchem.get_hydrophobicity(molsys, definition='eisenberg')
    rao = msm.physchem.get_hydrophobicity(molsys, definition='rao')
    sweet = msm.physchem.get_hydrophobicity(molsys, definition='sweet')
    kyte = msm.physchem.get_hydrophobicity(molsys, definition='kyte')
    abraham = msm.physchem.get_hydrophobicity(molsys, definition='abraham')
    bull = msm.physchem.get_hydrophobicity(molsys, definition='bull')
    guy = msm.physchem.get_hydrophobicity(molsys, definition='guy')
    miyazawa = msm.physchem.get_hydrophobicity(molsys, definition='miyazawa')
    roseman = msm.physchem.get_hydrophobicity(molsys, definition='roseman')
    wolfenden = msm.physchem.get_hydrophobicity(molsys, definition='wolfenden')
    chothia = msm.physchem.get_hydrophobicity(molsys, definition='chothia')
    hopp = msm.physchem.get_hydrophobicity(molsys, definition='hopp')
    manavalan = msm.physchem.get_hydrophobicity(molsys, definition='manavalan')
    black = msm.physchem.get_hydrophobicity(molsys, definition='black')
    fauchere = msm.physchem.get_hydrophobicity(molsys, definition='fauchere')

    assert len(eisenberg)==n_groups

