"""Preparing state-specific covalent graphs and sparse cycle memberships."""

import networkx as nx
import numpy as np

from molsysmt._private.smonitor import (
    ArgumentError,
    StructuralInconsistencyError,
    UnsupportedHeavyOperationError,
)
from molsysmt._private.sparse_membership import pack_membership, whole_group_selection


def ring_context(molecular_system, chemical_state, structure_indices, assume_complete, caller):
    """Resolve chemistry without selecting or truncating the source covalent graph."""
    from molsysmt._private.h5msm import modular_h5msm_dimensions
    from molsysmt._private.variables import is_all
    from molsysmt.basic import convert, get_form
    from molsysmt.native import ChemicalStates, MolSys, Topology

    selection_frames = structure_indices
    dimensions = modular_h5msm_dimensions(molecular_system)
    if dimensions is not None:
        from molsysmt.form._h5msm05_modular import _read_calculation_chemistry

        frames = np.arange(dimensions[1], dtype=np.int64) if is_all(structure_indices) else structure_indices
        if np.any(np.asarray(frames) < 0) or np.any(np.asarray(frames) >= dimensions[1]):
            raise ArgumentError("structure_indices", value=structure_indices, caller=caller)
        molecular_system, chemical_state = _read_calculation_chemistry(
            molecular_system, chemical_state=chemical_state, structure_indices=frames,
            require_topology=False,
        )
        selection_frames = "all"
    if chemical_state == "structure":
        if not isinstance(molecular_system, MolSys):
            raise ArgumentError("chemical_state", value=chemical_state, caller=caller)
        chemical_state = molecular_system._resolve_structure_chemical_state_index(structure_indices)
    if isinstance(molecular_system, MolSys):
        states = molecular_system.chemical_states
    elif isinstance(molecular_system, ChemicalStates):
        states = molecular_system
    elif get_form(molecular_system) == "molsysmt.ChemicalStatesDict":
        molecular_system = convert(molecular_system, to_form="molsysmt.ChemicalStates")
        states = molecular_system
    else:
        topology = (
            molecular_system if isinstance(molecular_system, Topology)
            else convert(molecular_system, to_form="molsysmt.Topology")
        )
        states = topology._chemical_states_domain
    if states is None:
        raise StructuralInconsistencyError(reason="A chemical-states domain is required.", caller=caller)
    state_index = states._resolve_index(None if chemical_state == "reference" else chemical_state)
    state = states._states[state_index]
    n_atoms = states.n_atoms
    if n_atoms and state.connectivity_completeness != "complete" and not assume_complete:
        raise StructuralInconsistencyError(
            reason="Ring perception requires connectivity declared complete.", caller=caller,
        )
    bonds = state.bonds
    if len(bonds):
        if not {"bond_type", "atom1_index", "atom2_index"} <= set(bonds.columns):
            raise StructuralInconsistencyError(reason="Bond chemistry columns are missing.", caller=caller)
        relationships = bonds["bond_type"]
        if relationships.isna().any() or not relationships.isin(["covalent", "dative"]).all():
            raise StructuralInconsistencyError(
                reason="Every bond requires a covalent or dative relationship.", caller=caller,
            )
        covalent = bonds.loc[relationships == "covalent"]
        pairs = covalent[["atom1_index", "atom2_index"]].to_numpy(dtype=np.int64)
    else:
        covalent, pairs = bonds, np.empty((0, 2), dtype=np.int64)
    if (
        np.any(pairs < 0) or np.any(pairs >= n_atoms)
        or np.any(pairs[:, 0] == pairs[:, 1])
        or len(np.unique(np.sort(pairs, axis=1), axis=0)) != len(pairs)
    ):
        raise StructuralInconsistencyError(
            reason="Covalent bonds must be unique pairs of distinct valid atom indices.", caller=caller,
        )
    return molecular_system, states, state, state_index, covalent, pairs, selection_frames


def minimum_cycle_memberships(pairs, max_cyclic_block_size, caller):
    """Find an unweighted basis per cyclic biconnected block with stable insertion order."""
    graph = nx.Graph()
    graph.add_edges_from(sorted(map(tuple, np.sort(pairs, axis=1).tolist())))
    rings = []
    for nodes in sorted(nx.biconnected_components(graph), key=lambda block: tuple(sorted(block))):
        if len(nodes) < 3:
            continue
        if len(nodes) > max_cyclic_block_size:
            raise UnsupportedHeavyOperationError(
                operation=caller, form="cyclic covalent graph",
                reason="A cyclic biconnected block exceeds max_cyclic_block_size; explicitly increase the limit after assessing cycle-basis cost.",
            )
        block = nx.Graph()
        block.add_nodes_from(sorted(nodes))
        block.add_edges_from(sorted(graph.subgraph(nodes).edges()))
        rings.extend(tuple(sorted(cycle)) for cycle in nx.minimum_cycle_basis(block))
    return [np.asarray(ring, dtype=np.int64) for ring in sorted(rings)]


def ring_result(rings, *, molecular_system, states, state, state_index,
                selection, selection_frames, syntax, assume_complete, method, caller):
    """Filter complete memberships and retain source axes and recognition evidence."""
    import networkx

    from molsysmt import __version__
    from molsysmt._private.variables import is_all
    from molsysmt.basic import convert, select
    from molsysmt.native import ChemicalStates, MolSys, Topology

    if isinstance(molecular_system, ChemicalStates) or (
        isinstance(molecular_system, MolSys) and molecular_system.topology is None
    ) or (
        not isinstance(molecular_system, (MolSys, Topology))
        and (not isinstance(selection, str) or is_all(selection))
    ):
        # A shallow collection view selects chemistry without copying or mutating records.
        from copy import copy

        molecular_system = copy(states)
        molecular_system._reference_index = state_index
        selection_state = "reference"
    elif not isinstance(molecular_system, (MolSys, Topology)):
        molecular_system = convert(molecular_system, to_form="molsysmt.MolSys")
        selection_state = state_index
    else:
        selection_state = state_index
    selected = select(
        molecular_system, selection=selection, structure_indices=selection_frames,
        chemical_state=selection_state, syntax=syntax,
    )
    if selected is None or np.asarray(selected).ndim != 1:
        raise ArgumentError("selection", value=selection, caller=caller)
    selected = np.unique(selected).astype(np.int64)
    included = whole_group_selection(rings, selected, caller=caller, description="perceived ring")
    retained = [rings[index] for index in np.flatnonzero(included)]
    atoms, offsets = pack_membership(retained)
    source_indices = np.arange(states.n_atoms, dtype=np.int64)
    return {
        "atom_indices": atoms, "atom_offsets": offsets,
        "n_atoms": states.n_atoms, "source_atom_indices": source_indices,
        "selection_atom_indices": selected, "examined_atom_indices": source_indices.copy(),
        "chemical_state_index": state_index, "method": method,
        "evidence": {
            "kind": "declared_covalent_connectivity",
            "connectivity_completeness": state.connectivity_completeness,
            "assume_complete_connectivity": assume_complete,
            "chemical_state_provenance_index": state.provenance_index,
        },
        "software": {"molsysmt": __version__, "networkx": networkx.__version__},
    }
