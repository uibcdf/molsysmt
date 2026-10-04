"""Classifying source bonds under explicit graph-based torsion criteria."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError


@signal(tags=["api", "topology"])
@arg_digest()
def get_rotatable_bonds(
    molecular_system,
    selection="all",
    structure_indices="all",
    chemical_state="reference",
    method="conjugation_restricted",
    syntax="MolSysMT",
    skip_digestion=False,
):
    """Classifying acyclic torsion candidates before filtering source bonds.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form supplying elements, complete covalent connectivity
        and supported bond orders. This graph criterion does not certify valence.
    selection : str, list, tuple or numpy.ndarray, default='all'
        Atoms to return. Classification uses the full source graph first;
        returned bonds require both endpoints in the selection.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Structure indices (0-based) for selection and state resolution only.
        The classifier does not use coordinates.
    chemical_state : str or int, default='reference'
        State supplying bond chemistry. 'structure' requires one resolved state
        across the requested structures.
    method : str, default='conjugation_restricted'
        Both methods require a single, nonaromatic bridge between nonterminal
        heavy atoms, neither incident to a triple bond. 'conjugation_restricted'
        additionally excludes C(=N/O/S)-N/O/S bonds. 'acyclic_single' retains them.
    syntax : str, default='MolSysMT'
        Syntax used for atom selection.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    dict
        Source bond_indices and bonded_atom_pairs, aligned bool is_rotatable,
        uint8 exclusion_mask and named exclusion_bits, plus eligible
        rotatable_bond_indices and rotatable_bonded_atom_pairs. Source atoms,
        evaluated scope, state, versioned criteria, evidence and original producer
        versions are retained. Empty pairs have shape (0, 2). No units apply.

    Raises
    ------
    ArgumentError
        If the method, state, selection or structure request is invalid.
    StructuralInconsistencyError
        If elements, complete connectivity or supported orders are unavailable,
        an aromatic bridge is declared, or dative chemistry is present.

    Notes
    -----
    Experimental graph policies, not energy/barrier calculations or exact RDKit
    Strict/Meeko reproductions. Heavy degree excludes H, so materializing the same
    H inventory does not change heavy-bond eligibility. Ring detection uses
    bridges of the original graph, without enumerating cycles. Amide, thioamide,
    amidine, ester and thioester links are restricted by the second policy;
    tertiary-amide symmetry exceptions are not applied. Charged resonance forms,
    biaryl hindrance and symmetry-equivalent terminal groups are not normalized.
    No aromaticity, charges, H or torsion tree is assigned. RDKit is unnecessary
    for native inputs; it may be needed by their chosen form conversion.
    Numeric H5MSM selections read chemistry; rich selections may load coordinates.
    Coordinates and source chemistry remain unchanged. Optional attribution
    failures preserve results. Consumers choose active cuts and export roots.

    See Also
    --------
    get_rigid_fragments : Partition complete connectivity at explicit chosen cuts.
    get_rings : Perceive a minimum covalent cycle basis.

    Examples
    --------
    >>> import molsysmt as msm
    >>> result = msm.topology.get_rotatable_bonds(
    ...     msm.systems['caffeine']['caffeine.sdf'])
    >>> result['rotatable_bond_indices'].tolist()
    []

    .. admonition:: User guide

       See :ref:`Tutorial_Rotatable_Bonds` for criteria and source correspondence.

    .. versionadded:: 1.0.0
    """
    from copy import deepcopy

    import networkx as nx
    import numpy as np
    import pandas as pd

    from molsysmt import __version__, _ackredit
    from molsysmt._private.variables import is_all
    from molsysmt.basic import get_form
    from molsysmt.topology._chemical_graph import (
        chemical_graph_context,
        detached_chemical_graph_view,
        select_chemical_atoms,
        validate_chemical_frames,
    )

    caller = "molsysmt.topology.get_rotatable_bonds"
    if not isinstance(skip_digestion, bool):
        from molsysmt._private.argdigest.argument.skip_digestion import (
            digest_skip_digestion,
        )

        digest_skip_digestion(skip_digestion, caller=caller)
    if method not in ("acyclic_single", "conjugation_restricted"):
        raise ArgumentError("method", value=method, caller=caller)
    original, original_frames = molecular_system, structure_indices
    input_form = get_form(molecular_system)
    conversion_software = {}
    if input_form == "rdkit.Mol":
        from rdkit import Chem, rdBase

        conversion_software["rdkit"] = rdBase.rdkitVersion

        if any(atom.HasQuery() for atom in molecular_system.GetAtoms()) or any(
            bond.HasQuery() for bond in molecular_system.GetBonds()
        ):
            raise StructuralInconsistencyError(
                reason="Torsion classification requires a concrete graph, not queries.",
                caller=caller,
            )
        # Conversion can assign stereo properties; never expose the caller's graph.
        molecular_system = Chem.Mol(molecular_system)
        original = molecular_system
    source, states, state, index, covalent, pairs, frames = chemical_graph_context(
        molecular_system, chemical_state, structure_indices, False, caller
    )
    frames = validate_chemical_frames(source, frames, caller)
    view = detached_chemical_graph_view(source, states, index, caller)
    symbols = view.topology.atoms["atom_type"]
    allowed = {"H", "B", "C", "N", "O", "F", "Si", "P", "S", "Cl", "Br", "I"}
    if not symbols.isin(allowed).all() or len(covalent) != len(state.bonds):
        raise StructuralInconsistencyError(
            reason="Torsion criteria require supported element symbols and covalent bonds; metals/dative chemistry are outside this route.",
            caller=caller,
        )
    orders = covalent.get("bond_order", pd.Series(np.nan, index=covalent.index))
    aromatic = covalent.get("is_aromatic", pd.Series(False, index=covalent.index))
    aromatic = aromatic.fillna(False).to_numpy(dtype=bool)
    if not (orders.isin([1, 2, 3]).to_numpy() | aromatic).all():
        raise StructuralInconsistencyError(
            reason="Every source bond needs a supported order or an explicit aromatic declaration.",
            caller=caller,
        )
    orders = orders.to_numpy(dtype=float, na_value=np.nan)
    graph = nx.Graph()
    graph.add_nodes_from(range(states.n_atoms))
    graph.add_edges_from(pairs)
    bridges = {tuple(sorted(pair)) for pair in nx.bridges(graph)}
    in_ring = np.asarray(
        [tuple(sorted(pair)) not in bridges for pair in pairs], dtype=bool
    )
    if np.any(aromatic & ~in_ring):
        raise StructuralInconsistencyError(
            reason="A declared aromatic bond cannot be a bridge in a complete covalent graph.",
            caller=caller,
        )
    heavy = symbols.ne("H").to_numpy()
    heavy_degree = np.zeros(states.n_atoms, dtype=np.int64)
    triple_endpoint = np.zeros(states.n_atoms, dtype=bool)
    carbon_multiple_hetero = np.zeros(states.n_atoms, dtype=bool)
    elements = symbols.to_numpy()
    for (left, right), order, is_aromatic in zip(pairs, orders, aromatic):
        heavy_degree[left] += heavy[right]
        heavy_degree[right] += heavy[left]
        if order == 3 and not is_aromatic:
            triple_endpoint[[left, right]] = True
        if order == 2 and not is_aromatic:
            for carbon, hetero in ((left, right), (right, left)):
                if elements[carbon] == "C" and elements[hetero] in {"N", "O", "S"}:
                    carbon_multiple_hetero[carbon] = True
    restricted = np.zeros(len(pairs), dtype=bool)
    if method == "conjugation_restricted":
        for i, (left, right) in enumerate(pairs):
            restricted[i] = (
                any(
                    carbon_multiple_hetero[carbon]
                    and elements[hetero] in {"N", "O", "S"}
                    for carbon, hetero in ((left, right), (right, left))
                )
                and orders[i] == 1
                and not aromatic[i]
            )
    flags = {
        "hydrogen_endpoint": ~heavy[pairs].all(axis=1),
        "not_single": (orders != 1) | aromatic,
        "ring_bond": in_ring,
        "terminal_heavy_atom": (heavy_degree[pairs] <= 1).any(axis=1),
        "adjacent_triple_bond": triple_endpoint[pairs].any(axis=1),
        "restricted_conjugation": restricted,
    }
    bits = {name: 1 << i for i, name in enumerate(flags)}
    mask = np.zeros(len(pairs), dtype=np.uint8)
    for name, flag in flags.items():
        mask[flag] |= bits[name]
    rich = isinstance(selection, str) and not is_all(selection)
    selected = select_chemical_atoms(
        original if rich else source,
        states,
        index,
        selection,
        original_frames if rich else frames,
        syntax,
    )
    chosen = np.flatnonzero(np.isin(pairs, selected).all(axis=1)).astype(np.int64)
    eligible = chosen[mask[chosen] == 0]
    references = [
        dict(
            id="rdkit-torsion-criteria-reference",
            type="software",
            title="RDKit rotatable-bond definitions: NonStrict, Strict and StrictLinkages",
            revision="cbfb37abddcd5b5feeac97d53530ae6be83cac0d",
            url="https://github.com/rdkit/rdkit/blob/cbfb37abddcd5b5feeac97d53530ae6be83cac0d/Code/GraphMol/Descriptors/Lipinski.cpp",
            roles=["reference_implementation"],
        ),
        dict(
            id="meeko-torsion-criteria-reference",
            type="software",
            title="Meeko BondTyperLegacy torsion criteria",
            version="0.8.0",
            revision="1eac18bd6d1111f35f9f1abaa8af502c2668d054",
            url="https://github.com/forlilab/Meeko/blob/1eac18bd6d1111f35f9f1abaa8af502c2668d054/meeko/bondtyper.py",
            roles=["reference_implementation"],
        ),
    ]
    software = dict(molsysmt=__version__, numpy=np.__version__, networkx=nx.__version__)
    software.update(conversion_software)
    items = deepcopy(references)
    for name, version in software.items():
        items.append(
            dict(
                id=f"software:{name}:{version}",
                type="software",
                title=name,
                version=version,
                roles=["executed_software"],
            )
        )
    with _ackredit.scope(caller) as provider:
        _ackredit.credit(provider, items, caller)
    return dict(
        schema="molsysmt.rotatable_bonds@1",
        atom_indices=selected,
        bond_indices=chosen,
        bonded_atom_pairs=pairs[chosen],
        is_rotatable=mask[chosen] == 0,
        exclusion_mask=mask[chosen],
        exclusion_bits=bits,
        rotatable_bond_indices=eligible,
        rotatable_bonded_atom_pairs=pairs[eligible],
        evaluated_atom_indices=np.arange(states.n_atoms, dtype=np.int64),
        evaluated_bond_indices=np.arange(len(pairs), dtype=np.int64),
        chemical_state_index=index,
        chemical_state_id=state.state_id,
        input_form=input_form,
        method=method,
        rule_version=f"{method}@1",
        parameters=dict(
            degree="heavy_neighbors",
            exclude_triple_endpoints=True,
            restrict_carbon_double_hetero_links=method == "conjugation_restricted",
        ),
        evidence="declared_complete_graph_with_explicit_torsion_criteria",
        software=software,
        references=references,
        attribution=dict(
            schema="molsysmt.scientific_attribution@1", target=caller, items=items
        ),
    )
