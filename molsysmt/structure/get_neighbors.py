from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_iterable_of_iterables
from molsysmt import pyunitwizard as puw
from molsysmt._private.lists import sorted_list_of_pairs
from molsysmt._private.smonitor import ArgumentConflictError, InternalAlgorithmError, NotImplementedMethodError
import numpy as np
from smonitor import signal


def _threshold_neighbors_via_cell_list(molecular_system, selection, selection_2,
                                       structure_indices, pbc, threshold, same_set):
    """Threshold-mode neighbour search via the shared cell-list primitive.

    Returns ``(neighs, dists)`` object arrays with the same contract as the
    ``get_distances``-based path (per query element: neighbour indices and
    distances sorted by ascending distance, self excluded for a self-search), or
    ``None`` when the cell-list cannot serve the request (e.g. non-positive
    cutoff), so the caller can fall back to the distance-matrix path.
    """
    from molsysmt.basic import get
    from molsysmt.lib.structure.neighbor_list import neighbor_list_csr

    q = get(molecular_system, element='atom', selection=selection,
            structure_indices=structure_indices, coordinates=True)
    length_units = puw.get_unit(q)
    q_val = np.ascontiguousarray(puw.get_value(q), dtype=np.float64)

    threshold_val = puw.get_value(threshold, to_unit=length_units)
    if not (threshold_val > 0.0):
        return None

    if same_set:
        r_val = None
    else:
        r = get(molecular_system, element='atom', selection=selection_2,
                structure_indices=structure_indices, coordinates=True)
        r_val = np.ascontiguousarray(puw.get_value(r), dtype=np.float64)

    box = None
    if pbc:
        box_q = get(molecular_system, element='system',
                    structure_indices=structure_indices, box=True)
        if box_q is not None and box_q[0] is not None:
            box = np.ascontiguousarray(puw.get_value(box_q, to_unit=length_units), dtype=np.float64)

    nstructures = q_val.shape[0]
    nelements_1 = q_val.shape[1]
    neighs = np.empty((nstructures, nelements_1), dtype=object)
    dists = np.empty((nstructures, nelements_1), dtype=object)

    for s in range(nstructures):
        box_s = box[s] if box is not None else None
        ref_s = None if same_set else r_val[s]
        offsets, indices, dd = neighbor_list_csr(
            q_val[s], ref_s, box=box_s, cutoff=threshold_val,
            exclude_self=same_set, return_distances=True)
        for ii in range(nelements_1):
            a = indices[offsets[ii]:offsets[ii + 1]]
            d = dd[offsets[ii]:offsets[ii + 1]]
            order = np.lexsort((a, d))  # by distance, ties broken by ascending index
            neighs[s, ii] = a[order]
            dists[s, ii] = d[order]

    dists = dists * length_units
    return neighs, dists


@signal(tags=['api', 'structure'])
@arg_digest()
def get_neighbors(molecular_system, selection="all", structure_indices="all", center_of_atoms=False, weights=None,
                  molecular_system_2=None, selection_2=None, structure_indices_2=None, center_of_atoms_2=False, weights_2=None,
                  threshold=None, n_neighbors=None, pairs=False, unique_pairs=False, mutual_only=False, pbc=True,
                  output_type='numpy.ndarray', output_indices=None, output_structure_indices=None,
                  sorted=True, engine='MolSysMT', syntax='MolSysMT', skip_digestion=False):
    """
    Find the neighbors of each atom (or group center) within a cutoff or by count.

    Exactly one of ``threshold`` or ``n_neighbors`` must be provided:

    * **Threshold mode** (``threshold`` is set, ``n_neighbors=None``): returns all
      neighbors whose distance is less than or equal to the cutoff.  The neighbor
      array has dtype ``object`` because each atom may have a different neighbor
      count.
    * **Fixed-count mode** (``n_neighbors`` is set, ``threshold=None``): returns the
      ``n_neighbors`` nearest neighbors for each atom as a fixed-size integer array.

    When ``selection_2`` is ``None`` and ``structure_indices_2`` is ``None`` the
    same set is used as both query and target (self-neighbor search).  Self-matches
    (distance ≈ 0) are automatically excluded in this case.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any form supported by MolSysMT.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Query atoms (or atom groups when ``center_of_atoms=True``).
    structure_indices : 'all' or array-like, default 'all'
        Frame indices of the query system.
    center_of_atoms : bool, default False
        If ``True``, use the (weighted) centroid of each group in ``selection``
        rather than individual atom positions.
    weights : array-like, optional
        Per-atom weights for centroid computation of the first selection.
    molecular_system_2 : molecular system or None, default None
        Second system used as the neighbor pool.  When ``None``, the same system
        is used.
    selection_2 : str, list, tuple or numpy.ndarray or None, default None
        Atoms in the neighbor pool.  When ``None``, the same selection and system
        are used (self-neighbor search).
    structure_indices_2 : 'all', array-like or None, default None
        Frame indices for the neighbor pool.  When ``None``, ``structure_indices``
        is reused.
    center_of_atoms_2 : bool, default False
        If ``True``, use the (weighted) centroid of each group in ``selection_2``.
    weights_2 : array-like, optional
        Per-atom weights for centroid computation of the second selection.
    threshold : str, quantity or None, default None
        Distance cutoff for the neighbor search.  Accepts any PyUnitWizard-parseable
        length quantity (e.g. ``'5 angstroms'``).  Mutually exclusive with
        ``n_neighbors``.
    n_neighbors : int or None, default None
        Number of nearest neighbors to return for each query element.  Mutually
        exclusive with ``threshold``.
    pairs : bool, default False
        If ``True``, ``selection`` is interpreted as an array of pre-defined pairs
        (not yet implemented for the neighbor output path).
    unique_pairs : bool, default False
        If ``True`` and ``output_type='pairs'``, each unordered pair is reported
        only once.
    mutual_only : bool, default False
        If ``True`` and ``output_type='pairs'``, only pairs where both atoms list
        each other as neighbors are returned.
    pbc : bool, default True
        Whether to apply periodic boundary conditions.  The actual PBC state is
        queried from the system; this flag disables the query when set to ``False``.
    output_type : {'numpy.ndarray', 'pairs'}, default 'numpy.ndarray'
        Format of the returned neighbor data.

        * ``'numpy.ndarray'``: return ``(neighs, dists)`` arrays directly.
        * ``'pairs'``: return a list of ``[query_idx, neighbor_idx]`` pairs per
          frame together with the corresponding distances.
    output_indices : {None, 'selection', 'atom'}, default None
        Index convention used in ``'pairs'`` output mode.
    output_structure_indices : array-like or None, default None
        Structure indices to include in the output metadata (passed through to
        ``get_distances``).
    sorted : bool, default True
        If ``True`` and ``output_type='pairs'``, pairs are returned in sorted order.
    engine : {'MolSysMT'}, default 'MolSysMT'
        Backend used for distance computation.
    syntax : str, default 'MolSysMT'
        Selection syntax used when selections are strings.
    skip_digestion : bool, default False
        Whether to skip argument digestion (for internal use on trusted hot paths).

    Returns
    -------
    neighs : numpy.ndarray or list
        Neighbor indices per query element per frame.  Shape is
        ``(n_structures, n_elements_1, n_neighbors)`` (fixed-count mode) or
        ``(n_structures, n_elements_1)`` with dtype ``object`` (threshold mode)
        when ``output_type='numpy.ndarray'``.
        A list of ``[query_idx, neighbor_idx]`` pairs per frame when
        ``output_type='pairs'``.
    dists : quantity or list
        Corresponding distances as a PyUnitWizard length quantity (numpy array
        output) or a list of quantities per frame (pairs output).

    Raises
    ------
    ArgumentConflictError
        If both ``threshold`` and ``n_neighbors`` are set, or neither is set.
    NotImplementedMethodError
        For output-type/index combinations not yet implemented.
    InternalAlgorithmError
        If a self-neighbor search detects an inconsistency in the distance matrix
        (i.e., the nearest neighbor of an element is not itself).

    .. versionadded:: 1.0.0
    """

    from . import get_distances
    from molsysmt.basic import select
    from molsysmt.pbc import has_pbc

    if pbc:
        pbc=has_pbc(molecular_system)

    same_set = False

    same_selections = False
    same_structures = False

    if (selection is not None) and (selection_2 is None):
        same_selections = True

    if structure_indices_2 is None:
        same_structures = True

    same_set= same_selections and same_structures

    # Fast path: threshold-mode atom neighbour search via the shared cell-list
    # primitive (O(N) vs the full O(N*M) distance matrix). Restricted to the
    # cases whose contract it reproduces exactly; everything else falls back.
    if (engine == 'MolSysMT' and threshold is not None and n_neighbors is None
            and output_type == 'numpy.ndarray'
            and output_indices is None and output_structure_indices is None
            and not center_of_atoms and not center_of_atoms_2
            and molecular_system_2 is None and structure_indices_2 is None
            and not pairs and weights is None and weights_2 is None
            and not is_iterable_of_iterables(selection)
            and not is_iterable_of_iterables(selection_2)):
        _cell_list_result = _threshold_neighbors_via_cell_list(
            molecular_system, selection, selection_2, structure_indices, pbc,
            threshold, same_set)
        if _cell_list_result is not None:
            return _cell_list_result

    output_get_distances = get_distances(molecular_system=molecular_system, selection=selection,
               structure_indices=structure_indices, center_of_atoms=center_of_atoms, weights=weights,
               selection_2=selection_2, structure_indices_2=structure_indices_2, center_of_atoms_2=center_of_atoms_2,
               output_type='numpy.ndarray', output_indices=output_indices, output_structure_indices=output_structure_indices,
               weights_2=weights_2, pbc=pbc, engine=engine, syntax=syntax)

    if output_indices is None and output_structure_indices is None:
        all_dists = output_get_distances
    else:
        all_dists = output_get_distances[-1]

    nstructures, nelements_1, nelements_2 = all_dists.shape
    length_units = puw.get_unit(all_dists)
    all_dists = puw.get_value(all_dists)

    if n_neighbors is not None and threshold is None:

        neighs=np.empty((nstructures, nelements_1, n_neighbors), dtype=int)
        dists=np.empty((nstructures, nelements_1, n_neighbors), dtype=float)

        offset = 0
        if same_set:
            offset = 1

        for indice_structure in range(nstructures):
            for ii in range(nelements_1):
                neighs_aux = np.argpartition(all_dists[indice_structure,ii,:], n_neighbors-1+offset)[:n_neighbors+offset]
                dists_aux = all_dists[indice_structure,ii,neighs_aux]
                good_order = np.argsort(dists_aux)
                neighs_aux = neighs_aux[good_order]
                dists_aux = dists_aux[good_order]
                neighs[indice_structure,ii,:]=neighs_aux[offset:]
                dists[indice_structure,ii,:]=dists_aux[offset:]
                if same_set:
                    if dists_aux[0] > 0.01:
                        raise InternalAlgorithmError(
                            reason="Sets are different in distance calculation for the same molecular system.",
                            caller="molsysmt.structure.get_neighbors"
                        )

        del(all_dists)

        dists=dists*length_units

    elif threshold is not None and n_neighbors is None:

        threshold = puw.get_value(threshold, to_unit=length_units)

        neighs=np.empty((nstructures, nelements_1), dtype=object)
        dists=np.empty((nstructures, nelements_1), dtype=object)

        offset = 0
        if same_set:
            offset = 1

        for indice_structure in range(nstructures):
            for ii in range(nelements_1):
                neighs_aux = np.argwhere(all_dists[indice_structure,ii,:]<=threshold)[:,0]
                dists_aux = all_dists[indice_structure,ii,neighs_aux]
                good_order = np.argsort(dists_aux)
                neighs_aux = neighs_aux[good_order]
                dists_aux = dists_aux[good_order]
                neighs[indice_structure,ii]=neighs_aux[offset:]
                dists[indice_structure,ii]=dists_aux[offset:]
                if same_set:
                    if dists_aux[0] > 0.01:
                        raise InternalAlgorithmError(
                            reason="Sets are different in distance calculation for the same molecular system.",
                            caller="molsysmt.structure.get_neighbors"
                        )

        del(all_dists)

        dists=dists*length_units

    else:

        raise ArgumentConflictError(
            arg1="threshold",
            arg2="n_neighbors",
            reason="Either threshold or n_neighbors must be provided, but not both at the same time.",
            caller="molsysmt.structure.get_neighbors"
        )

    if output_type == 'numpy.ndarray':
        if output_indices is None and output_structure_indices is None:
            return neighs, dists
        else:
            raise NotImplementedMethodError(caller='molsysmt.structure.get_neighbors')
    elif output_type == 'pairs':
        with_output_indices = False
        if output_indices is not None:
            with_output_indices = True
            if len(output_get_distances)==2:
                aux_indices_1 = output_get_distances[0]
                aux_indices_2 = aux_indices_1
            elif len(output_get_distances)==3:
                aux_indices_1 = output_get_distances[0]
                aux_indices_2 = output_get_distances[1]
            else:
                raise NotImplementedMethodError(caller='molsysmt.structure.get_neighbors')
        if output_indices is not None:
            neighs_pairs = []
            dists_pairs = []
            for ii in range(nstructures):
                aux_pairs = []
                aux_dists = []
                for jj in range(nelements_1):
                    for kk in range(len(neighs[ii,jj])):
                        aux_dists.append(dists[ii,jj][kk])
                        if with_output_indices:
                            aux_pairs.append([aux_indices_1[jj], aux_indices_2[neighs[ii,jj][kk]]])
                        else:
                            aux_pairs.append([jj, neighs[ii,jj][kk]])
                if mutual_only:
                    tmp_pairs = []
                    tmp_dists = []
                    for pair, dist in zip(aux_pairs, aux_dists):
                        if ([pair[1], pair[0]] in aux_pairs) and (pair[0]<pair[1]):
                            tmp_pairs.append(pair)
                            tmp_dists.append(dist)
                    aux_pairs = tmp_pairs
                    aux_dists = tmp_dists
                if unique_pairs:
                    tmp_pairs = []
                    tmp_dists = []
                    for pair, dist in zip(aux_pairs, aux_dists):
                        if [pair[0],pair[1]] not in tmp_pairs and [pair[1],pair[0]] not in tmp_pairs:
                            tmp_pairs.append(pair)
                            tmp_dists.append(dist)
                    aux_pairs = tmp_pairs
                    aux_dists = tmp_dists
                if len(aux_dists)>0:
                    aux_dists = puw.utils.sequences.concatenate(aux_dists, value_type='list')
                if sorted:
                    aux_pairs, aux_dists = sorted_list_of_pairs(aux_pairs, aux_dists)
                neighs_pairs.append(aux_pairs)
                dists_pairs.append(aux_dists)
            return neighs_pairs, dists_pairs
        else:
            raise NotImplementedMethodError(caller='molsysmt.structure.get_neighbors')

    raise InternalAlgorithmError(
        reason="The function reached an unreachable state.",
        caller="molsysmt.structure.get_neighbors"
    )
