"""
Unit and regression tests for get_rmsf on molsysmt.MolSys molecular systems.
"""

import molsysmt as msm
from molsysmt import systems
import numpy as np


def test_get_rmsf_shape():
    molsys = msm.convert(systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    rmsf = msm.structure.get_rmsf(molsys, selection='backbone')
    rmsf_val = msm.pyunitwizard.get_value(rmsf, to_unit='nm')
    n_backbone = msm.get(molsys, element='atom', selection='backbone', n_atoms=True)
    assert rmsf_val.shape == (n_backbone,)


def test_get_rmsf_values():
    molsys = msm.convert(systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    rmsf = msm.structure.get_rmsf(molsys, selection='backbone')
    rmsf_val = msm.pyunitwizard.get_value(rmsf, to_unit='nm')
    expected = np.array([0.72103537, 0.73506875, 0.64748055, 0.56723117, 0.46837355])
    assert np.allclose(rmsf_val[:5], expected, atol=1e-4)


def test_get_rmsf_single_structure_is_zero():
    """RMSF of a single structure relative to itself must be zero."""
    molsys = msm.convert(systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')
    rmsf = msm.structure.get_rmsf(molsys, selection='backbone')
    rmsf_val = msm.pyunitwizard.get_value(rmsf, to_unit='nm')
    assert np.allclose(rmsf_val, 0.0, atol=1e-10)


def test_get_rmsf_heavy_mode_matches_eager():
    """Streaming RMSF agrees with eager execution across multiple chunks."""

    path = systems['pentalanine']['traj_pentalanine.h5msm']
    molsys = msm.convert(path, to_form='molsysmt.MolSys')
    structure_indices = list(range(0, 5000, 37))
    eager = msm.structure.get_rmsf(
        molsys,
        selection="backbone",
        structure_indices=structure_indices,
        heavy_mode="off",
    )
    chunked = msm.structure.get_rmsf(
        path,
        selection="backbone",
        structure_indices=structure_indices,
        heavy_mode="force",
    )

    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(chunked, to_unit="nm"),
        msm.pyunitwizard.get_value(eager, to_unit="nm"),
        rtol=0.0,
        atol=1.0e-12,
    )
