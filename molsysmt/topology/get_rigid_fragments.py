"""Partitioning a covalent graph at explicitly selected active bonds."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError


@signal(tags=["api", "topology"])
@arg_digest()
def get_rigid_fragments(
    molecular_system,
    bond_indices=None,
    chemical_state="reference",
    structure_indices="all",
    skip_digestion=False,
):
    """Deriving rigid fragments by cutting explicitly selected covalent bonds.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported form with a complete covalent graph.
    bond_indices : int, list, tuple or numpy.ndarray, default=None
        Source bond indices (0-based) to cut. None cuts no bonds. Repeated
        indices are deduplicated. Dative and ring cuts are rejected.
    chemical_state : str, int or None, default='reference'
        Chemical state supplying connectivity. 'structure' resolves the state
        assigned to the selected structures; these must agree on one state.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Structure indices (0-based) used only for chemical-state resolution.
    skip_digestion : bool, default=False
        Whether to skip argument digestion. Default is False.

    Returns
    -------
    dict
        Packed int64 fragment_atom_indices and fragment_offsets, a fragment
        index for each source atom (atom_fragment_indices), selected source
        bond_indices and bonded_atom_pairs, and aligned fragment_pairs. Also
        includes atom_indices, chemical_state_index and connectivity evidence.
        Fragments and their memberships are sorted by source atom index.

    Raises
    ------
    ArgumentError
        If a cut is out of range, noncovalent, or does not separate its endpoints.
    StructuralInconsistencyError
        If complete, valid chemical connectivity is unavailable.

    Notes
    -----
    Rigidity here means connectivity after the supplied cuts. This function
    does not classify chemically rotatable bonds, impose torsion angles or
    root a PDBQT tree. Bond orders are not needed for explicit graph cuts.
    Every selected bond must be a bridge in the original covalent graph;
    cutting multiple ring edges does not make them eligible torsions.
    Coordinates and the source chemical state are not modified.

    See Also
    --------
    get_covalent_blocks : Find connected atom sets after removing atom pairs.
    get_rings : Perceive a minimum cycle basis from declared connectivity.

    Examples
    --------
    >>> import molsysmt as msm
    >>> import pandas as pd
    >>> from molsysmt.native import Topology
    >>> topology = Topology(n_atoms=3)
    >>> topology.bonds = pd.DataFrame({'atom1_index': [0, 1],
    ...     'atom2_index': [1, 2], 'bond_type': ['covalent', 'covalent']})
    >>> topology._chemical_states[0].connectivity_completeness = 'complete'
    >>> result = msm.topology.get_rigid_fragments(topology, bond_indices=[1])
    >>> result['fragment_atom_indices'].tolist(), result['fragment_offsets'].tolist()
    ([0, 1, 2], [0, 2, 3])

    .. admonition:: Tutorial with more examples

       See :ref:`Tutorial_Rigid_Fragments` for explicit graph cuts.

    .. versionadded:: 1.0.0
    """
    import networkx as nx
    import numpy as np

    from molsysmt.topology._chemical_graph import chemical_graph_context

    caller = "molsysmt.topology.get_rigid_fragments"
    _, states, state, state_index, covalent, pairs, _ = chemical_graph_context(
        molecular_system, chemical_state, structure_indices, False, caller
    )
    cuts = np.asarray([] if bond_indices is None else bond_indices)
    if cuts.ndim != 1 or (cuts.size and cuts.dtype.kind not in "iu"):
        raise ArgumentError("bond_indices", value=bond_indices, caller=caller)
    cuts = np.unique(cuts).astype(np.int64)
    if (
        np.any(cuts < 0)
        or np.any(cuts >= len(state.bonds))
        or not np.isin(cuts, covalent.index).all()
    ):
        raise ArgumentError("bond_indices", value=bond_indices, caller=caller)
    cut_pairs = (
        state.bonds.loc[cuts, ["atom1_index", "atom2_index"]]
        .to_numpy(dtype=np.int64)
        .reshape(-1, 2)
    )
    graph = nx.Graph()
    graph.add_nodes_from(range(states.n_atoms))
    graph.add_edges_from(pairs)
    if len(cuts):
        bridges = {tuple(sorted(pair)) for pair in nx.bridges(graph)}
        if any(tuple(sorted(pair)) not in bridges for pair in cut_pairs):
            raise ArgumentError(
                "bond_indices",
                value=bond_indices,
                caller=caller,
                message="Each active cut must be a bridge of the original covalent graph.",
            )
    graph.remove_edges_from(cut_pairs)
    blocks = nx.connected_components(graph)
    fragments = sorted((sorted(block) for block in blocks), key=lambda block: block[0])
    packed = np.asarray([atom for block in fragments for atom in block], dtype=np.int64)
    offsets = np.asarray(
        [0, *np.cumsum([len(block) for block in fragments])], dtype=np.int64
    )
    labels = np.empty(states.n_atoms, dtype=np.int64)
    for index, block in enumerate(fragments):
        labels[block] = index
    return {
        "atom_indices": np.arange(states.n_atoms, dtype=np.int64),
        "fragment_atom_indices": packed,
        "fragment_offsets": offsets,
        "atom_fragment_indices": labels,
        "bond_indices": cuts,
        "bonded_atom_pairs": cut_pairs,
        "fragment_pairs": labels[cut_pairs],
        "chemical_state_index": state_index,
        "connectivity_completeness": state.connectivity_completeness,
        "evidence": "declared_graph_with_explicit_cuts",
    }
