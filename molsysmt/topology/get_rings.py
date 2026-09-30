"""Perceiving sparse ring memberships from a declared covalent graph."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError


@signal(tags=["api", "topology"])
@arg_digest()
def get_rings(
    molecular_system,
    selection="all",
    structure_indices="all",
    chemical_state="reference",
    method="minimum_cycle_basis",
    assume_complete_connectivity=False,
    syntax="MolSysMT",
    skip_digestion=False,
    *,
    max_cyclic_block_size=256,
):
    """Perceiving a minimum cycle basis of one chemical state's covalent graph.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system with a stable atom domain and declared covalent connectivity.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atom selection. Include every atom of each intersected perceived ring.
        Perception precedes selection; source atom indices are preserved.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) used for selections and state resolution.
        No coordinates or per-structure occurrences are calculated.
    chemical_state : {'reference', 'structure'}, int, or None, default='reference'
        State supplying bonds. Structure-assigned states must resolve to one
        state across the requested structures. None selects the reference.
    method : str, default='minimum_cycle_basis'
        Unweighted NetworkX minimum cycle basis of the complete covalent graph.
        Dative bonds are excluded. This basis is not an enumeration of all cycles.
    assume_complete_connectivity : bool, default=False
        Declare supplied connectivity complete when metadata is insufficient.
        Record this assumption without modifying the source.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate selection.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    max_cyclic_block_size : int, default=256
        Keyword-only maximum atoms per cyclic biconnected block. Raise before
        basis calculation for a larger block. Acyclic chains are unrestricted.
        Increasing this limit can substantially increase time and memory.

    Returns
    -------
    dict
        Packed int64 atom_indices and atom_offsets, source and selected atom
        indices, examined scope, chemical_state_index, method, connectivity
        evidence, and producer versions. Memberships are sorted atom sets,
        not traversal order. Empty arrays have (0,) and offsets equal [0].

    Raises
    ------
    ArgumentError
        If the method, block limit, state, or a partial-ring selection is invalid.
    StructuralInconsistencyError
        If the atom domain or complete, valid covalent connectivity is unavailable.
    UnsupportedHeavyOperationError
        If a cyclic block exceeds max_cyclic_block_size.

    Notes
    -----
    This experimental tool describes connectivity, without inferring aromaticity
    from bond order, residue names, coordinates, or planarity. Full source
    chemistry is examined before selection. H5MSM 0.5 index selections load
    chemistry without coordinates or saved analyses. Spatial string selections
    on that metadata-only route require loading the system explicitly first.
    Equal-weight bases need not be unique or preserve molecular symmetry. Sorted
    graph insertion and memberships make results reproducible for fixed source
    indices and NetworkX version; atom reordering can change a tied basis.
    The block limit bounds individual problems, not process RSS or runtime.
    ChemicalStates, ChemicalStatesDict and topology-free MolSys inputs also
    support membership calculations when their stored chemistry is sufficient.

    See Also
    --------
    molsysmt.physchem.get_aromatic_rings
        Perceiving cycles specifically in the declared aromatic bond graph.
    molsysmt.topology.get_bondgraph
        Returning a graph for general connectivity inspection.

    Examples
    --------
    >>> import molsysmt as msm
    >>> import pandas as pd
    >>> from molsysmt.native import Topology
    >>> from molsysmt.topology.get_rings import get_rings
    >>> molsys = Topology(n_atoms=3)
    >>> molsys.bonds = pd.DataFrame({'atom1_index': [0, 1, 2],
    ...     'atom2_index': [1, 2, 0], 'bond_type': ['covalent'] * 3})
    >>> rings = get_rings(molsys, assume_complete_connectivity=True)
    >>> rings['atom_indices'].tolist(), rings['atom_offsets'].tolist()
    ([0, 1, 2], [0, 3])

    .. admonition:: User guide

       See :ref:`Getting rings <Tutorial_Get_rings>`.

    .. versionadded:: 1.0.0
    """
    from molsysmt.topology._rings import (
        minimum_cycle_memberships,
        ring_context,
        ring_result,
    )

    caller = "molsysmt.topology.get_rings"
    if method != "minimum_cycle_basis":
        raise ArgumentError("method", value=method, caller=caller)
    source, states, state, state_index, _, pairs, frames = ring_context(
        molecular_system, chemical_state, structure_indices, assume_complete_connectivity, caller,
    )
    rings = minimum_cycle_memberships(pairs, max_cyclic_block_size, caller)
    result = ring_result(
        rings, molecular_system=source, states=states, state=state, state_index=state_index,
        selection=selection, selection_frames=frames, syntax=syntax,
        assume_complete=assume_complete_connectivity, method=method, caller=caller,
    )
    result["max_cyclic_block_size"] = max_cyclic_block_size
    return result
