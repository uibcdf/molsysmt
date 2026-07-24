"""
Parity tests for the cell-list fast path of get_neighbors threshold mode against
an independent full distance-matrix reference (the pre-migration algorithm).
"""

import molsysmt as msm
from molsysmt import systems
import numpy as np

puw = msm.pyunitwizard


def _reference(ms, selection, selection_2, threshold, pbc):
    """Threshold neighbours (indices + distances) via the full distance matrix."""
    all_dists = msm.structure.get_distances(ms, selection=selection, selection_2=selection_2, pbc=pbc)
    units = puw.get_unit(all_dists)
    dmat = puw.get_value(all_dists)
    thr = puw.get_value(puw.quantity(threshold), to_unit=units)
    same = selection_2 is None
    ns, n1, _ = dmat.shape
    neighs = np.empty((ns, n1), dtype=object)
    dists = np.empty((ns, n1), dtype=object)
    for s in range(ns):
        for ii in range(n1):
            w = np.argwhere(dmat[s, ii, :] <= thr)[:, 0]
            order = np.argsort(dmat[s, ii, w])
            w = w[order]
            dd = dmat[s, ii, w]
            if same:
                w = w[1:]
                dd = dd[1:]
            neighs[s, ii] = w
            dists[s, ii] = dd
    return neighs, dists


def _assert_parity(ms, selection, selection_2, threshold, pbc):
    neighs, dists = msm.structure.get_neighbors(ms, selection=selection, selection_2=selection_2,
                                                threshold=threshold, pbc=pbc)
    ref_neighs, ref_dists = _reference(ms, selection, selection_2, threshold, pbc)
    units = puw.get_unit(dists)
    dists_val = puw.get_value(dists)
    ns, n1 = neighs.shape
    for s in range(ns):
        for ii in range(n1):
            got = np.asarray(neighs[s, ii])
            # Same neighbour set.
            assert set(got.tolist()) == set(ref_neighs[s, ii].tolist())
            # Distances aligned with the returned neighbours, and sorted ascending.
            got_d = np.asarray(dists_val[s, ii])
            assert np.all(np.diff(got_d) >= -1e-9)
            # Per-neighbour distance matches the reference distance for that index.
            ref_map = {int(j): d for j, d in zip(ref_neighs[s, ii], ref_dists[s, ii])}
            for j, d in zip(got.tolist(), got_d.tolist()):
                assert np.isclose(d, ref_map[int(j)], atol=1e-6)


def test_get_neighbors_cell_list_self_vacuum():
    ms = msm.convert(systems['Trp-Cage']['1l2y.h5msm'], to_form='molsysmt.MolSys')
    ms = msm.extract(ms, structure_indices=[0, 1])
    _assert_parity(ms, 'all', None, '5 angstroms', pbc=False)


def test_get_neighbors_cell_list_disjoint_vacuum():
    ms = msm.convert(systems['Trp-Cage']['1l2y.h5msm'], to_form='molsysmt.MolSys')
    ms = msm.extract(ms, structure_indices=[0])
    _assert_parity(ms, 'atom_index < 100', 'atom_index >= 100', '6 angstroms', pbc=False)


def test_get_neighbors_cell_list_self_pbc():
    ms = msm.convert(systems['pentalanine']['traj_pentalanine.h5msm'], to_form='molsysmt.MolSys')
    ms = msm.extract(ms, structure_indices=[0, 1, 2])
    _assert_parity(ms, 'all', None, '5 angstroms', pbc=True)
