"""Match chemical SMARTS on complete declared source graphs."""

import numpy as np
from depdigest import dep_digest
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import (
    ArgumentError,
    MemoryBudgetExceededError,
    StructuralInconsistencyError,
)


@signal(tags=["api", "topology"])
@arg_digest()
@dep_digest("rdkit")
def get_substructure_matches(
    molecular_system,
    patterns,
    selection="all",
    structure_indices="all",
    chemical_state="reference",
    assume_complete_connectivity=False,
    syntax="MolSysMT",
    skip_digestion=False,
    *,
    max_matches=100000,
):
    """Matching chemical SMARTS without truncating or changing the source atom axis.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form supplying elements, complete connectivity, bond
        orders, formal charges and explicit aromatic atom/bond flags.
    patterns : str, list, or tuple
        One SMARTS query or a sequence of queries, evaluated in supplied order.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Retain only matches whose atoms all belong to this atom selection.
        The full graph is matched before filtering; chemistry is not truncated.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices for state resolution and coordinate-based selections.
        No coordinates are required for index selections or 'all'.
    chemical_state : {'reference', 'structure'}, int, or None, default='reference'
        State supplying chemistry. Structure assignments must resolve one state.
    assume_complete_connectivity : bool, default=False
        Record an explicit assumption of completeness without filling bonds.
    syntax : str, default='MolSysMT'
        Syntax used to evaluate selection.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    max_matches : int, default=100000
        Keyword-only maximum unique matches per query before atom filtering.
        Exceeding it raises instead of silently returning a truncated result.

    Returns
    -------
    dict
        patterns and matches are aligned tuples. Each match matrix has int64
        shape (n_matches, n_query_atoms), including (0, n_query_atoms) when
        empty. Columns preserve SMARTS query order; values are source atom
        indices, not IDs. Metadata retains source/selection axes, selected
        chemistry, RDKit/MolSysMT versions and declared chemistry evidence.

    Raises
    ------
    ArgumentError
        If a query or match limit is invalid.
    StructuralInconsistencyError
        If required chemistry is absent, contradictory or changed by RDKit
        sanitization. Atomic elements require a topology inventory.
    UnsupportedHeavyOperationError
        If a query exceeds max_matches. No truncated result is returned.
    MemoryBudgetExceededError
        If bounded matching or its resident numeric output exceeds the budget.

    Notes
    -----
    This experimental tool uses RDKit's uniquified SMARTS matches and ring
    perception, including its implicit-hydrogen/valence interpretation. It does
    not invent missing formal charge or aromatic metadata. Native chemistry is
    converted through the existing chemistry-aware RDKit adapter without a
    structural series; RDKit input retains its atom-level hydrogen declarations.
    Sanitization must preserve declared formal charge and aromatic flags.
    Pattern ordering is preserved, not canonicalized across different graphs.
    Numeric matching reserves one quarter of configure.max_ram_usage; source
    graphs and Python overhead are outside this estimate. RDKit is optional.

    See Also
    --------
    molsysmt.physchem.get_aromatic_rings
        Perceiving a declared aromatic minimum cycle basis instead of SMARTS.
    molsysmt.topology.get_rings
        Perceiving covalent rings irrespective of aromaticity.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt.topology.get_substructure_matches import get_substructure_matches
    >>> from rdkit import Chem
    >>> matches = get_substructure_matches(Chem.MolFromSmiles('CCO'), ['[O]', '[N]'])
    >>> [matrix.tolist() for matrix in matches['matches']]
    [[[2]], []]
    >>> matches['matches'][1].shape
    (0, 1)

    .. admonition:: User guide

       See :ref:`Getting substructure matches <Tutorial_Get_substructure_matches>`.

    .. versionadded:: 1.0.0
    """
    import pandas as pd
    from rdkit import Chem, rdBase

    from molsysmt import __version__, configure
    from molsysmt._private.smonitor import UnsupportedHeavyOperationError
    from molsysmt._private.variables import is_all
    from molsysmt.basic import convert, get_form, select
    from molsysmt.native import MolSys, Topology
    from molsysmt.physchem.atoms.mass import physical as elements
    from molsysmt.topology._rings import ring_context

    caller = "molsysmt.topology.get_substructure_matches"
    source, states, state, state_index, _, _, frames = ring_context(
        molecular_system,
        chemical_state,
        structure_indices,
        assume_complete_connectivity,
        caller,
    )
    attributes, bonds = state.atom_attributes, state.bonds
    for name in ("formal_charge", "is_aromatic"):
        if states.n_atoms and (name not in attributes or attributes[name].isna().any()):
            raise StructuralInconsistencyError(
                reason=f"Every atom requires explicit {name} metadata.", caller=caller
            )
    if len(bonds) and ("is_aromatic" not in bonds or bonds["is_aromatic"].isna().any()):
        raise StructuralInconsistencyError(
            reason="Every bond requires an explicit is_aromatic flag.", caller=caller
        )
    if len(bonds):
        covalent = bonds.loc[bonds["bond_type"] == "covalent"]
        orders = covalent.reindex(columns=["bond_order", "fractional_bond_order"])
        values = orders["bond_order"].to_numpy(dtype=float, na_value=np.nan, copy=True)
        fractional = orders["fractional_bond_order"].to_numpy(
            dtype=float, na_value=np.nan
        )
        values[np.isnan(values)] = fractional[np.isnan(values)]
        values[covalent["is_aromatic"].to_numpy(dtype=bool)] = 1.5
        if not np.isin(values, np.arange(1.0, 6.5, 0.5)).all():
            raise StructuralInconsistencyError(
                reason="Every covalent bond requires a supported declared order.",
                caller=caller,
            )
    if get_form(source) == "rdkit.Mol":
        molecule = Chem.Mol(source)
        selection_source = source
    else:
        topology = (
            source.topology
            if isinstance(source, MolSys)
            else source
            if isinstance(source, Topology)
            else convert(source, to_form="molsysmt.Topology")
        )
        if topology is None:
            raise StructuralInconsistencyError(
                reason="SMARTS matching requires an explicit element inventory.",
                caller=caller,
            )
        symbols = topology.atoms["atom_type"].to_numpy(dtype=object)
        if any(pd.isna(symbol) or symbol not in elements for symbol in symbols):
            raise StructuralInconsistencyError(
                reason="Every atom requires an explicit element symbol.", caller=caller
            )
        # copy.copy(Topology) invokes compatibility restoration on shared
        # chemistry. Construct the read-only inventory view without that hook.
        view = object.__new__(type(topology))
        view.__dict__ = topology.__getstate__()
        state_view = states.copy()
        state_view._reference_index = state_index
        view._chemical_states_domain = state_view
        chemical_source = MolSys._from_partial_domains(
            topology=view, chemical_states=state_view
        )
        molecule = convert(chemical_source, to_form="rdkit.Mol")
        selection_source = source
    if (
        molecule.GetNumAtoms() != states.n_atoms
        or [atom.GetFormalCharge() for atom in molecule.GetAtoms()]
        != (
            attributes["formal_charge"].tolist()
            if "formal_charge" in attributes
            else []
        )
        or [atom.GetIsAromatic() for atom in molecule.GetAtoms()]
        != (attributes["is_aromatic"].tolist() if "is_aromatic" in attributes else [])
    ):
        raise StructuralInconsistencyError(
            reason="RDKit changed the declared atom axis, charges or aromaticity.",
            caller=caller,
        )
    if len(bonds):
        for _, bond in bonds.iterrows():
            rd_bond = molecule.GetBondBetweenAtoms(
                int(bond["atom1_index"]), int(bond["atom2_index"])
            )
            if rd_bond is None or rd_bond.GetIsAromatic() != bool(bond["is_aromatic"]):
                raise StructuralInconsistencyError(
                    reason="RDKit changed declared bond aromaticity.", caller=caller
                )
    if not isinstance(selection, str) or is_all(selection):
        selection_source = states.copy()
        selection_source._reference_index = state_index
        selection_state = "reference"
    else:
        selection_source = (
            source
            if isinstance(source, (MolSys, Topology))
            else convert(source, to_form="molsysmt.MolSys")
        )
        selection_state = state_index
    selected = np.unique(
        select(
            selection_source,
            selection=selection,
            structure_indices=frames,
            chemical_state=selection_state,
            syntax=syntax,
        )
    ).astype(np.int64)
    selected_mask = np.zeros(states.n_atoms, dtype=bool)
    selected_mask[selected] = True
    output, used = [], selected_mask.nbytes
    budget = configure.max_ram_usage // 4
    for pattern in patterns:
        query = Chem.MolFromSmarts(pattern)
        if query is None or query.GetNumAtoms() == 0:
            raise ArgumentError(
                "patterns",
                value=pattern,
                caller=caller,
                message="Use a nonempty valid SMARTS query.",
            )
        width = query.GetNumAtoms()
        numeric_limit = max(0, (budget - used) // (128 + 8 * width))
        bound = min(max_matches, numeric_limit)
        matches = molecule.GetSubstructMatches(
            query, uniquify=True, maxMatches=int(bound + 1)
        )
        if len(matches) > bound:
            if bound < max_matches:
                raise MemoryBudgetExceededError(
                    reason="SMARTS matching exceeds its bounded working estimate.",
                    predicted_bytes=used + len(matches) * (128 + 8 * width),
                    available_bytes=budget,
                    caller=caller,
                )
            raise UnsupportedHeavyOperationError(
                operation=caller,
                form="RDKit SMARTS matches",
                reason="The query exceeds max_matches; increase the explicit limit after assessing cost.",
            )
        array = np.asarray(matches, dtype=np.int64).reshape(-1, width)
        array = array[selected_mask[array].all(axis=1)]
        output.append(array)
        used += array.nbytes
    return dict(
        patterns=patterns,
        matches=tuple(output),
        n_atoms=states.n_atoms,
        source_atom_indices=np.arange(states.n_atoms, dtype=np.int64),
        selection_atom_indices=selected,
        chemical_state_index=state_index,
        method="rdkit_uniquified_smarts",
        max_matches=max_matches,
        evidence={
            "kind": "declared_chemical_graph",
            "connectivity_completeness": state.connectivity_completeness,
            "assume_complete_connectivity": assume_complete_connectivity,
            "chemical_state_provenance_index": state.provenance_index,
        },
        software={"molsysmt": __version__, "rdkit": rdBase.rdkitVersion},
    )
