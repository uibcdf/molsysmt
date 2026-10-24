import numpy as np
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import (
    ArgumentConflictError,
    ArgumentError,
    InternalAlgorithmError,
    NotImplementedMethodError,
)
from molsysmt._private.variables import is_iterable_of_iterables
from molsysmt.configure import with_configure_overrides


def _threshold_neighbors_via_cell_list(
    molecular_system,
    selection,
    selection_2,
    structure_indices,
    pbc,
    threshold,
    same_set,
    output_type,
):
    """Threshold-mode neighbour search via the shared multi-structure cell list.

    The heavy work (search, distances, per-atom sort) runs in a single parallel
    kernel over the flattened (structure, atom) space. Returns either object arrays
    ``(neighs, dists)`` (``output_type='numpy.ndarray'``) assembled by cheap
    slicing, or the flat CSR ``(offsets, indices, distances)`` (``'csr'``). Returns
    ``None`` when the cell list cannot serve the request (non-positive cutoff), so
    the caller can fall back to the distance-matrix path.
    """
    from molsysmt._private.rust_backend import neighbor_list_csr_multi
    from molsysmt.basic import get

    from .get_distances import _validate_boxes, _validate_coordinate_pair

    q = get(
        molecular_system,
        element="atom",
        selection=selection,
        structure_indices=structure_indices,
        coordinates=True,
    )
    length_units = puw.get_unit(q)
    q_val = np.ascontiguousarray(puw.get_value(q), dtype=np.float64)

    threshold_val = puw.get_value(threshold, to_unit=length_units)
    if not (threshold_val > 0.0):
        return None

    if same_set:
        r_val = None
    else:
        r = get(
            molecular_system,
            element="atom",
            selection=selection_2,
            structure_indices=structure_indices,
            coordinates=True,
        )
        r_val = np.ascontiguousarray(puw.get_value(r), dtype=np.float64)

    box = None
    if pbc:
        box_q = get(
            molecular_system,
            element="system",
            structure_indices=structure_indices,
            box=True,
        )
        if box_q is not None and box_q[0] is not None:
            box = np.ascontiguousarray(
                puw.get_value(box_q, to_unit=length_units), dtype=np.float64
            )

    _validate_coordinate_pair(q_val, r_val)
    if box is not None:
        _validate_boxes(box, len(q_val))
    if (
        q_val.shape[0] == 0
        or q_val.shape[1] == 0
        or (r_val is not None and r_val.shape[1] == 0)
    ):
        offsets = np.zeros(q_val.shape[0] * q_val.shape[1] + 1, dtype=np.int64)
        indices, distances = np.empty(0, dtype=np.int64), np.empty(0, dtype=float)
    else:
        offsets, indices, distances = neighbor_list_csr_multi(
            q_val,
            r_val,
            box=box,
            cutoff=threshold_val,
            exclude_self=same_set,
            sort_by_distance=True,
        )

    if output_type == "csr":
        return offsets, indices, distances * length_units

    nstructures = q_val.shape[0]
    nelements_1 = q_val.shape[1]
    neighs = np.empty((nstructures, nelements_1), dtype=object)
    dists = np.empty((nstructures, nelements_1), dtype=object)
    for s in range(nstructures):
        row = s * nelements_1
        for ii in range(nelements_1):
            w = row + ii
            neighs[s, ii] = indices[offsets[w] : offsets[w + 1]]
            dists[s, ii] = distances[offsets[w] : offsets[w + 1]]

    dists = dists * length_units
    return neighs, dists


@signal(tags=["api", "structure"])
@arg_digest()
@with_configure_overrides
def get_neighbors(
    molecular_system,
    selection="all",
    structure_indices="all",
    center_of_atoms=False,
    weights=None,
    molecular_system_2=None,
    selection_2=None,
    structure_indices_2=None,
    center_of_atoms_2=False,
    weights_2=None,
    threshold=None,
    n_neighbors=None,
    pairs=False,
    unique_pairs=False,
    mutual_only=False,
    pbc=True,
    output_type="numpy.ndarray",
    output_indices=None,
    output_structure_indices=None,
    sorted=True,
    engine="MolSysMT",
    syntax="MolSysMT",
    parallel=None,
    num_threads=None,
    skip_digestion=False,
):
    """
    Finding the neighbors of each atom (or group center) within a cutoff or by count.

    Exactly one of ``threshold`` or ``n_neighbors`` must be provided:

    * **Threshold mode** (``threshold`` is set, ``n_neighbors=None``): returns all
      neighbors whose distance is less than or equal to the cutoff.  The neighbor
      array has dtype ``object`` because each atom may have a different neighbor
      count.
    * **Fixed-count mode** (``n_neighbors`` is set, ``threshold=None``): returns the
      ``n_neighbors`` nearest neighbors for each atom as a fixed-size integer array.

    With no explicit second endpoint definition, the selected population
    supplies both endpoints. Self identity is excluded; distinct coincident atoms
    remain neighbors. An explicit second system is always an independent source.
    Neighbors sort by distance, breaking ties by local target index.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    center_of_atoms : bool, default=False
        Whether to compute distances relative to geometric centers.
    weights : numpy.ndarray, list, or tuple, default=None
        Atomic mass weights array for center calculation.
    molecular_system_2 : molecular system or None, default=None
        Second molecular system to compare with the first one.
    selection_2 : str, list, tuple, or numpy.ndarray, default=None
        Second selection string or boolean/integer array.
    structure_indices_2 : int, list, tuple, or numpy.ndarray, default=None
        Structure indices (0-based) for the second selection.
    center_of_atoms_2 : bool, default=False
        Whether to compute distances relative to geometric centers for selection_2.
    weights_2 : numpy.ndarray, list, or tuple, default=None
        Atomic mass weights array for selection_2.
    threshold : float or quantity, default=None
        Distance cutoff threshold quantity.
    n_neighbors : int or None, default=None
        Maximum number of nearest neighbors returned for each selected element.
    pairs : bool, default=False
        Whether corresponding selections define explicit pairs instead of a Cartesian product.
    unique_pairs : bool, default=False
        Whether to remove duplicate undirected neighbor pairs.
    mutual_only : bool, default=False
        Whether to retain only neighbor relations shared in both directions.
    pbc : bool, default=True
        Whether to take periodic boundary conditions into account.
    output_type : str, default='numpy.ndarray'
        Representation used for the returned result.
    output_indices : {'selection', 'atom', 'group'} or None, default=None
        Index convention included with the returned values.
    output_structure_indices : {'selection', 'structure'} or None, default=None
        Structure-index convention included with the returned values.
    sorted : bool, default=True
        Whether to order pair rows lexicographically, preserving query/target roles. Neighbor rows themselves are distance-sorted.
    engine : str, default='MolSysMT'
        Backend used to perform the calculation.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    parallel : bool or None, default=None
        Whether to use CPU parallelism, or `None` to use the configured default.
    num_threads : int or None, default=None
        Number of CPU worker threads, or `None` to use the configured default.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    neighs : numpy.ndarray or list
        Neighbor indices per query element per structure.  Shape is
        ``(n_structures, n_elements_1, n_neighbors)`` (fixed-count mode) or
        ``(n_structures, n_elements_1)`` with dtype ``object`` (threshold mode)
        when ``output_type='numpy.ndarray'``.
        A list of ``[query_idx, neighbor_idx]`` pairs per structure when
        ``output_type='pairs'``.
    dists : quantity or list
        Corresponding distances as a PyUnitWizard length quantity (numpy array
        output) or a list of quantities per structure (pairs output).


    Raises
    ------
    ArgumentConflictError
        If both ``threshold`` and ``n_neighbors`` are set, or neither is set.
    NotImplementedMethodError
        For output-type/index combinations not yet implemented.
    ArgumentError
        If a cutoff/count is invalid or the requested count exceeds available targets.


    Notes
    -----
    Counts can be zero. Thresholds are finite nonnegative scalar lengths and
    include the boundary. Returned indices refer to local target positions;
    pair output can request atom or selection labels. Pair filters require
    compatible node identities in one source; unsupported combinations and
    pairs=True reject explicitly. CSR is available only on the flat-atom
    threshold cell-list route. Internal disk distance storage is retired after
    reduction. The primary system supplies the periodic box.

    Examples
    --------
    >>> import molsysmt as msm
    >>> source = msm.systems['particles 4']['traj_particles_4.xyznpy']
    >>> indices, distances = get_neighbors(source, selection=[0],
    ...     selection_2=[1, 2], n_neighbors=1, pbc=False)
    >>> indices.shape
    (3, 1, 1)

    .. admonition:: User guide

       See :ref:`user-tools-distance-family`.

    .. versionadded:: 1.0.0
    """

    from molsysmt.pbc import has_pbc

    from . import get_distances

    caller = "molsysmt.structure.get_neighbors"
    if (threshold is None) == (n_neighbors is None):
        raise ArgumentConflictError(
            arg1="threshold",
            arg2="n_neighbors",
            reason="Provide exactly one of threshold or n_neighbors.",
            caller=caller,
        )
    if pairs or (
        (unique_pairs or mutual_only)
        and (output_type != "pairs" or molecular_system_2 is not None)
    ):
        raise NotImplementedMethodError(caller=caller)
    if n_neighbors is not None and (
        isinstance(n_neighbors, (bool, np.bool_)) or n_neighbors < 0
    ):
        raise ArgumentError(
            "n_neighbors",
            caller=caller,
            message="Neighbor counts must be nonnegative integers.",
        )
    if threshold is not None:
        cutoff = puw.get_value(threshold, to_unit="nm")
        if np.ndim(cutoff) != 0 or not np.isfinite(cutoff) or cutoff < 0:
            raise ArgumentError(
                "threshold",
                caller=caller,
                message="Cutoffs must be finite nonnegative scalar lengths.",
            )

    if pbc:
        pbc = has_pbc(molecular_system)

    same_set = False

    same_selections = False
    same_structures = False

    if (selection is not None) and (selection_2 is None):
        same_selections = True

    if structure_indices_2 is None:
        same_structures = True

    same_set = (
        molecular_system_2 is None
        and same_selections
        and same_structures
        and not center_of_atoms_2
        and weights_2 is None
    )
    if (unique_pairs or mutual_only) and output_indices != "atom" and not same_set:
        raise NotImplementedMethodError(caller=caller)

    self_labels = None
    if (
        same_set
        and not center_of_atoms
        and not is_iterable_of_iterables(selection)
        and not isinstance(selection, str)
    ):
        labels = np.atleast_1d(np.asarray(selection))
        if labels.dtype.kind in "iu" and len(np.unique(labels)) != len(labels):
            self_labels = labels

    # Fast path: threshold-mode atom neighbour search via the shared multi-structure
    # cell list (O(N) vs the full O(N*M) distance matrix). Restricted to the cases
    # whose contract it reproduces exactly; everything else falls back.
    _cell_list_eligible = (
        engine == "MolSysMT"
        and threshold is not None
        and n_neighbors is None
        and output_type in ("numpy.ndarray", "csr")
        and output_indices is None
        and output_structure_indices is None
        and self_labels is None
        and not center_of_atoms
        and not center_of_atoms_2
        and molecular_system_2 is None
        and structure_indices_2 is None
        and not pairs
        and weights is None
        and weights_2 is None
        and not (is_iterable_of_iterables(selection) and len(selection) > 0)
        and not (is_iterable_of_iterables(selection_2) and len(selection_2) > 0)
    )
    if _cell_list_eligible:
        _cell_list_result = _threshold_neighbors_via_cell_list(
            molecular_system,
            selection,
            selection_2,
            structure_indices,
            pbc,
            threshold,
            same_set,
            output_type,
        )
        if _cell_list_result is not None:
            return _cell_list_result

    if output_type == "csr":
        # 'csr' output is only produced by the cell-list fast path.
        raise NotImplementedMethodError(caller="molsysmt.structure.get_neighbors")

    output_get_distances = get_distances(
        molecular_system=molecular_system,
        molecular_system_2=molecular_system_2,
        selection=selection,
        structure_indices=structure_indices,
        center_of_atoms=center_of_atoms,
        weights=weights,
        selection_2=selection_2,
        structure_indices_2=structure_indices_2,
        center_of_atoms_2=center_of_atoms_2,
        output_type="numpy.ndarray",
        output_indices=output_indices,
        output_structure_indices=output_structure_indices,
        weights_2=weights_2,
        pbc=pbc,
        engine=engine,
        syntax=syntax,
    )

    if output_indices is None and output_structure_indices is None:
        all_dists = output_get_distances
    else:
        all_dists = output_get_distances[-1]

    nstructures, nelements_1, nelements_2 = all_dists.shape
    length_units = puw.get_unit(all_dists)
    all_dists = puw.get_value(all_dists)

    from molsysmt._private.execution.persistent_result import PersistentResultHandle

    try:
        excluded = int(same_set)
        if self_labels is not None:
            _, counts = np.unique(self_labels, return_counts=True)
            excluded = int(counts.max(initial=0))
        available = max(0, nelements_2 - excluded)
        if n_neighbors is not None and n_neighbors > available:
            raise ArgumentError(
                "n_neighbors",
                caller=caller,
                message="The requested count exceeds the available target population.",
            )
        if n_neighbors is not None:
            neighs = np.empty((nstructures, nelements_1, n_neighbors), dtype=int)
            dists = np.empty((nstructures, nelements_1, n_neighbors), dtype=float)
        else:
            threshold = puw.get_value(threshold, to_unit=length_units)
            neighs = np.empty((nstructures, nelements_1), dtype=object)
            dists = np.empty((nstructures, nelements_1), dtype=object)

        target_indices = np.arange(nelements_2)
        for structure in range(nstructures):
            for query in range(nelements_1):
                row = all_dists[structure, query, :]
                if self_labels is not None:
                    candidates = target_indices[self_labels != self_labels[query]]
                else:
                    candidates = (
                        target_indices[target_indices != query]
                        if same_set
                        else target_indices
                    )
                if n_neighbors is None:
                    candidates = candidates[row[candidates] <= threshold]
                elif n_neighbors == 0:
                    candidates = candidates[:0]
                elif n_neighbors < len(candidates):
                    values = row[candidates]
                    boundary = np.partition(values, n_neighbors - 1)[n_neighbors - 1]
                    closer = candidates[values < boundary]
                    ties = candidates[values == boundary][: n_neighbors - len(closer)]
                    candidates = np.concatenate((closer, ties))
                order = np.lexsort((candidates, row[candidates]))
                selected = candidates[order]
                neighs[structure, query] = selected
                dists[structure, query] = row[selected]
        dists = puw.quantity(dists, length_units)

    finally:
        if isinstance(all_dists, PersistentResultHandle):
            row = None
            all_dists.cleanup()

    if output_type == "numpy.ndarray":
        if output_indices is None and output_structure_indices is None:
            return neighs, dists
        else:
            raise NotImplementedMethodError(caller="molsysmt.structure.get_neighbors")
    elif output_type == "pairs":
        with_output_indices = False
        if output_indices is not None:
            with_output_indices = True
            if len(output_get_distances) == 2:
                aux_indices_1 = output_get_distances[0]
                aux_indices_2 = aux_indices_1
            elif len(output_get_distances) == 3:
                aux_indices_1 = output_get_distances[0]
                aux_indices_2 = output_get_distances[1]
            else:
                raise NotImplementedMethodError(
                    caller="molsysmt.structure.get_neighbors"
                )
        if output_indices is not None:
            neighs_pairs = []
            dists_pairs = []
            for ii in range(nstructures):
                aux_pairs = []
                aux_dists = []
                for jj in range(nelements_1):
                    for kk in range(len(neighs[ii, jj])):
                        aux_dists.append(dists[ii, jj][kk])
                        if with_output_indices:
                            aux_pairs.append(
                                [aux_indices_1[jj], aux_indices_2[neighs[ii, jj][kk]]]
                            )
                        else:
                            aux_pairs.append([jj, neighs[ii, jj][kk]])
                if mutual_only:
                    tmp_pairs = []
                    tmp_dists = []
                    for pair, dist in zip(aux_pairs, aux_dists):
                        if ([pair[1], pair[0]] in aux_pairs) and (pair[0] < pair[1]):
                            tmp_pairs.append(pair)
                            tmp_dists.append(dist)
                    aux_pairs = tmp_pairs
                    aux_dists = tmp_dists
                if unique_pairs:
                    tmp_pairs = []
                    tmp_dists = []
                    for pair, dist in zip(aux_pairs, aux_dists):
                        if [pair[0], pair[1]] not in tmp_pairs and [
                            pair[1],
                            pair[0],
                        ] not in tmp_pairs:
                            tmp_pairs.append(pair)
                            tmp_dists.append(dist)
                    aux_pairs = tmp_pairs
                    aux_dists = tmp_dists
                if len(aux_dists) > 0:
                    aux_dists = puw.utils.sequences.concatenate(
                        aux_dists, value_type="list"
                    )
                if sorted and aux_pairs:
                    labels = np.asarray(aux_pairs)
                    order = np.lexsort((labels[:, 1], labels[:, 0]))
                    aux_pairs = [aux_pairs[index] for index in order]
                    aux_dists = puw.utils.sequences.slice(
                        aux_dists, order, value_type="list"
                    )
                neighs_pairs.append(aux_pairs)
                dists_pairs.append(aux_dists)
            return neighs_pairs, dists_pairs
        else:
            raise NotImplementedMethodError(caller="molsysmt.structure.get_neighbors")

    raise InternalAlgorithmError(
        reason="The function reached an unreachable state.",
        caller="molsysmt.structure.get_neighbors",
    )
