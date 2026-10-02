"""Preparing state-specific covalent graphs and sparse cycle memberships."""

import networkx as nx
import numpy as np

from molsysmt._private.smonitor import (
    ArgumentError,
    UnsupportedHeavyOperationError,
)
from molsysmt._private.sparse_membership import pack_membership, whole_group_selection

# Existing ring tools share the general chemical graph boundary.
from molsysmt.topology._chemical_graph import chemical_graph_context

ring_context = chemical_graph_context


def minimum_cycle_memberships(pairs, max_cyclic_block_size, caller):
    """Find an unweighted basis per cyclic biconnected block with stable insertion order."""
    graph = nx.Graph()
    graph.add_edges_from(sorted(map(tuple, np.sort(pairs, axis=1).tolist())))
    rings = []
    for nodes in sorted(
        nx.biconnected_components(graph), key=lambda block: tuple(sorted(block))
    ):
        if len(nodes) < 3:
            continue
        if len(nodes) > max_cyclic_block_size:
            raise UnsupportedHeavyOperationError(
                operation=caller,
                form="cyclic covalent graph",
                reason="A cyclic biconnected block exceeds max_cyclic_block_size; explicitly increase the limit after assessing cycle-basis cost.",
            )
        block = nx.Graph()
        block.add_nodes_from(sorted(nodes))
        block.add_edges_from(sorted(graph.subgraph(nodes).edges()))
        rings.extend(tuple(sorted(cycle)) for cycle in nx.minimum_cycle_basis(block))
    return [np.asarray(ring, dtype=np.int64) for ring in sorted(rings)]


def ring_result(
    rings,
    *,
    molecular_system,
    states,
    state,
    state_index,
    selection,
    selection_frames,
    syntax,
    assume_complete,
    method,
    caller,
):
    """Filter complete memberships and retain source axes and recognition evidence."""
    import networkx

    from molsysmt import __version__
    from molsysmt._private.variables import is_all
    from molsysmt.basic import convert, select
    from molsysmt.native import ChemicalStates, MolSys, Topology

    if (
        isinstance(molecular_system, ChemicalStates)
        or (isinstance(molecular_system, MolSys) and molecular_system.topology is None)
        or (
            not isinstance(molecular_system, (MolSys, Topology))
            and (not isinstance(selection, str) or is_all(selection))
        )
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
        molecular_system,
        selection=selection,
        structure_indices=selection_frames,
        chemical_state=selection_state,
        syntax=syntax,
    )
    if selected is None or np.asarray(selected).ndim != 1:
        raise ArgumentError("selection", value=selection, caller=caller)
    selected = np.unique(selected).astype(np.int64)
    included = whole_group_selection(
        rings, selected, caller=caller, description="perceived ring"
    )
    retained = [rings[index] for index in np.flatnonzero(included)]
    atoms, offsets = pack_membership(retained)
    source_indices = np.arange(states.n_atoms, dtype=np.int64)
    return {
        "atom_indices": atoms,
        "atom_offsets": offsets,
        "n_atoms": states.n_atoms,
        "source_atom_indices": source_indices,
        "selection_atom_indices": selected,
        "examined_atom_indices": source_indices.copy(),
        "chemical_state_index": state_index,
        "method": method,
        "evidence": {
            "kind": "declared_covalent_connectivity",
            "connectivity_completeness": state.connectivity_completeness,
            "assume_complete_connectivity": assume_complete,
            "chemical_state_provenance_index": state.provenance_index,
        },
        "software": {"molsysmt": __version__, "networkx": networkx.__version__},
    }
