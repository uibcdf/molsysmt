"""
Unit and regression tests for get_secondary_structure on molsysmt.MolSys molecular systems
using the MDTraj engine.
"""

import molsysmt as msm
from molsysmt import systems
import numpy as np


def test_get_secondary_structure_shape():
    molsys = msm.convert(systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')
    ss = msm.structure.get_secondary_structure(molsys, simplified=True)
    n_groups = msm.get(molsys, element='system', n_groups=True)
    assert ss.shape == (1, n_groups)


def test_get_secondary_structure_simplified_codes():
    """All simplified DSSP codes should be H, E, C, or NA."""
    molsys = msm.convert(systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')
    ss = msm.structure.get_secondary_structure(molsys, simplified=True)
    allowed = {'H', 'E', 'C', 'NA'}
    assert set(np.unique(ss)).issubset(allowed)


def test_get_secondary_structure_simplified_counts():
    molsys = msm.convert(systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')
    ss = msm.structure.get_secondary_structure(molsys, simplified=True)
    unique, counts = np.unique(ss[0], return_counts=True)
    count_dict = dict(zip(unique.tolist(), counts.tolist()))
    assert count_dict.get('H', 0) == 106
    assert count_dict.get('E', 0) == 15
    assert count_dict.get('C', 0) == 41
    assert count_dict.get('NA', 0) == 140


def test_get_secondary_structure_full_codes():
    """Full DSSP codes should not all be simplified 3-state."""
    molsys = msm.convert(systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')
    ss_full = msm.structure.get_secondary_structure(molsys, simplified=False)
    ss_simp = msm.structure.get_secondary_structure(molsys, simplified=True)
    # full-mode has at least as many unique codes as simplified
    assert len(np.unique(ss_full)) >= len(np.unique(ss_simp))
