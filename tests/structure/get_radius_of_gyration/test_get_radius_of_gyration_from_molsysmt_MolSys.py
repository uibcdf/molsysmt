"""
Unit and regression tests for get_radius_of_gyration on molsysmt.MolSys molecular systems.
"""

import molsysmt as msm
from molsysmt import systems
import numpy as np


def test_get_radius_of_gyration_single_structure():
    molsys = msm.convert(systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')
    rg = msm.structure.get_radius_of_gyration(molsys, selection='atom_type!="H"')
    rg_val = msm.pyunitwizard.get_value(rg, to_unit='nm')
    assert rg_val.shape == (1,)
    assert np.allclose(rg_val, [1.6509885], atol=1e-4)


def test_get_radius_of_gyration_trajectory():
    molsys = msm.convert(systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    rg = msm.structure.get_radius_of_gyration(molsys, selection='atom_type!="H"',
                                              structure_indices=[0, 100])
    rg_val = msm.pyunitwizard.get_value(rg, to_unit='nm')
    assert rg_val.shape == (2,)
    assert np.allclose(rg_val, [0.49910624, 0.60989975], atol=1e-4)


def test_get_radius_of_gyration_uniform_vs_mass_weighted_differ():
    """Mass-weighted Rg should differ from geometric Rg for a heterogeneous system."""
    molsys = msm.convert(systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')
    rg_geom = msm.structure.get_radius_of_gyration(molsys, selection='atom_type!="H"', weights=None)
    rg_mass = msm.structure.get_radius_of_gyration(molsys, selection='atom_type!="H"', weights='masses')
    rg_geom_val = msm.pyunitwizard.get_value(rg_geom, to_unit='nm')
    rg_mass_val = msm.pyunitwizard.get_value(rg_mass, to_unit='nm')
    assert not np.allclose(rg_geom_val, rg_mass_val, atol=1e-6)
