"""Perceiving ring participants from explicit state-specific aromatic metadata."""

import numpy as np
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError


@signal(tags=["api", "physchem"])
@arg_digest()
def get_aromatic_rings(
    molecular_system,
    selection="all",
    structure_indices="all",
    chemical_state="reference",
    definition="stored_aromatic_bonds",
    method="minimum_cycle_basis",
    assume_complete_connectivity=False,
    syntax="MolSysMT",
    skip_digestion=False,
    *,
    max_cyclic_block_size=256,
):
    """Perceiving ring participants from explicitly declared aromatic covalent bonds.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system with an atom domain, complete connectivity, and explicit
        atom and bond is_aromatic attributes in the selected chemical state.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atom selection. Include all atoms of each intersected aromatic ring.
        Shared atoms can make a selection cut an adjacent fused ring.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) used for selections and state resolution.
        Recognition is chemical; no geometric occurrences are calculated.
    chemical_state : {'reference', 'structure'}, int, or None, default='reference'
        State supplying aromatic flags and bonds. Structure-assigned states
        must resolve to one state across all requested structures.
    definition : str, default='stored_aromatic_bonds'
        Use only covalent bonds explicitly marked aromatic, with explicitly
        aromatic endpoints. Do not infer or recalculate aromaticity.
    method : str, default='minimum_cycle_basis'
        Unweighted minimum cycle basis of the aromatic bond subgraph, rather
        than filtering a basis of the full covalent graph.
    assume_complete_connectivity : bool, default=False
        Declare supplied connectivity complete when metadata is insufficient.
        Record this assumption without changing the source.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate selection.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    max_cyclic_block_size : int, default=256
        Keyword-only maximum atoms per cyclic aromatic biconnected block.
        Increasing it can substantially increase basis time and memory.

    Returns
    -------
    dict
        Packed int64 atom_indices and atom_offsets for complete ring participants,
        original source axes, selection and examined scope, state index, method,
        definition, rule_version, evidence, and producer versions. Sorted atom
        memberships are not cyclic traversal order. Empty arrays have (0,)
        and offsets equal [0]. No coordinates or unit-bearing measures appear.

    Raises
    ------
    ArgumentError
        If a definition, method, state, block limit, or partial selection is invalid.
    StructuralInconsistencyError
        If required chemistry is missing, contradictory, or an aromatic bond
        does not belong to a cycle in the declared aromatic bond graph.
    UnsupportedHeavyOperationError
        If a cyclic aromatic block exceeds max_cyclic_block_size.

    Notes
    -----
    This experimental rule requires known atom and bond flags across the source,
    including explicit False for nonaromatic entries. Unknown is not False.
    A planar ring alone is not evidence of aromaticity. Atom flags alone do
    not classify bonds connecting aromatic atoms. Fused systems may contain
    nonaromatic fusion bonds; those bonds are omitted, so a perimeter cycle can
    be returned instead of its individual subrings. This is a declared-bond
    basis, not a universal aromaticity model, RDKit SymmSSSR, or every cycle.
    Tied bases can change with atom reordering or NetworkX version. Full chemistry
    is examined before selection; sources and reference states remain unchanged.
    H5MSM 0.5 index selections load chemistry without structural series or analyses;
    spatial string selections require explicitly loading the system first.
    ChemicalStates, ChemicalStatesDict and topology-free MolSys inputs can
    supply participants without a topology inventory. Legacy TopologyDict
    and MolSysDict forms do not supply complete aromatic metadata.

    See Also
    --------
    molsysmt.topology.get_rings
        Perceiving a basis from all covalent bonds irrespective of aromaticity.
    molsysmt.physchem.get_charge_centers
        Recognizing other reusable chemical participants.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt.native import Topology
    >>> from molsysmt.physchem.get_aromatic_rings import get_aromatic_rings
    >>> molsys = Topology(n_atoms=1)
    >>> msm.set(molsys, element='atom', atom_is_aromatic=[False])
    >>> rings = get_aromatic_rings(molsys, assume_complete_connectivity=True)
    >>> rings['atom_indices'].shape, rings['atom_offsets'].tolist()
    ((0,), [0])

    .. admonition:: User guide

       See :ref:`Getting aromatic rings <Tutorial_Get_aromatic_rings>`.

    .. versionadded:: 1.0.0
    """
    import networkx as nx

    from molsysmt.topology._rings import (
        minimum_cycle_memberships,
        ring_context,
        ring_result,
    )

    caller = "molsysmt.physchem.get_aromatic_rings"
    if definition != "stored_aromatic_bonds":
        raise ArgumentError("definition", value=definition, caller=caller)
    if method != "minimum_cycle_basis":
        raise ArgumentError("method", value=method, caller=caller)
    source, states, state, state_index, _, pairs, frames = ring_context(
        molecular_system, chemical_state, structure_indices, assume_complete_connectivity, caller,
    )
    attributes = state.atom_attributes
    if states.n_atoms and (
        "is_aromatic" not in attributes or attributes["is_aromatic"].isna().any()
    ):
        raise StructuralInconsistencyError(
            reason="Every atom requires an explicit is_aromatic flag.", caller=caller,
        )
    bonds = state.bonds
    if len(bonds) and ("is_aromatic" not in bonds or bonds["is_aromatic"].isna().any()):
        raise StructuralInconsistencyError(
            reason="Every bond requires an explicit is_aromatic flag.", caller=caller,
        )
    atom_aromatic = attributes["is_aromatic"].to_numpy(dtype=bool) if states.n_atoms else np.empty(0, dtype=bool)
    if len(bonds) and np.any(bonds["is_aromatic"] & (bonds["bond_type"] != "covalent")):
        raise StructuralInconsistencyError(
            reason="A dative bond cannot be a declared aromatic covalent bond.", caller=caller,
        )
    covalent = bonds.loc[bonds["bond_type"] == "covalent"] if len(bonds) else bonds
    flags = covalent["is_aromatic"].to_numpy(dtype=bool) if len(covalent) else np.empty(0, dtype=bool)
    aromatic_pairs = pairs[flags]
    if not np.all(atom_aromatic[aromatic_pairs]):
        raise StructuralInconsistencyError(
            reason="An aromatic covalent bond requires aromatic endpoint atoms.", caller=caller,
        )
    graph = nx.Graph()
    graph.add_edges_from(aromatic_pairs.tolist())
    if list(nx.bridges(graph)) or set(np.flatnonzero(atom_aromatic)) != set(graph.nodes):
        raise StructuralInconsistencyError(
            reason="Declared aromatic atoms and bonds must belong to aromatic cycles.", caller=caller,
        )
    rings = minimum_cycle_memberships(aromatic_pairs, max_cyclic_block_size, caller)
    result = ring_result(
        rings, molecular_system=source, states=states, state=state, state_index=state_index,
        selection=selection, selection_frames=frames, syntax=syntax,
        assume_complete=assume_complete_connectivity, method=method, caller=caller,
    )
    result.update({
        "definition": definition, "rule_version": "stored_aromatic_bond_cycles@1",
        "max_cyclic_block_size": max_cyclic_block_size,
    })
    result["evidence"]["kind"] = "chemical_states.is_aromatic"
    return result
