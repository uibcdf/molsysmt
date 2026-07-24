"""
Parity tests for the cell-list accelerated native SASA path
(``use_cell_list``) against the brute-force O(N^2) kernels. The cell-list only
restricts the occlusion candidate set, so results must be numerically identical.
"""

import molsysmt as msm
from molsysmt import systems
import numpy as np

puw = msm.pyunitwizard


def _atom_sasa(molsys, use_cell_list, structure_indices='all', n_sphere_points=100):
    sasa = msm.physchem.get_sasa(molsys, element='atom', engine='MolSysMT',
                                 n_sphere_points=n_sphere_points,
                                 structure_indices=structure_indices,
                                 use_cell_list=use_cell_list)
    return puw.get_value(sasa, to_unit='nm**2')


def test_cell_list_matches_brute_force_vacuum():
    molsys = msm.convert(systems['Trp-Cage']['1l2y.h5msm'], to_form='molsysmt.MolSys')
    brute = _atom_sasa(molsys, use_cell_list=False)
    cell = _atom_sasa(molsys, use_cell_list=True)
    assert np.allclose(brute, cell, atol=1e-9, rtol=0)


def test_cell_list_matches_brute_force_pbc():
    molsys = msm.convert(systems['pentalanine']['traj_pentalanine.h5msm'], to_form='molsysmt.MolSys')
    assert msm.pbc.has_pbc(molsys)
    frames = list(range(5))
    brute = _atom_sasa(molsys, use_cell_list=False, structure_indices=frames)
    cell = _atom_sasa(molsys, use_cell_list=True, structure_indices=frames)
    assert np.allclose(brute, cell, atol=1e-9, rtol=0)


def test_cell_list_auto_matches_explicit_on_small_system():
    # Below CELL_LIST_MIN_ATOMS, 'auto' falls back to brute force; either way the
    # numeric result must be identical.
    molsys = msm.convert(systems['Trp-Cage']['1l2y.h5msm'], to_form='molsysmt.MolSys')
    auto = _atom_sasa(molsys, use_cell_list='auto')
    explicit = _atom_sasa(molsys, use_cell_list=True)
    assert np.allclose(auto, explicit, atol=1e-9, rtol=0)
