"""Recognize ordered chemical sites for halogen-bond geometry."""

from depdigest import dep_digest
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.interaction_attribution import attributed


@signal(tags=["api", "physchem"])
@arg_digest()
@dep_digest("rdkit")
@attributed("halogen_bond_sites")
def get_halogen_bond_sites(
    molecular_system,
    selection="all",
    structure_indices="all",
    chemical_state="reference",
    method="smarts_donor_acceptor",
    assume_complete_connectivity=False,
    syntax="MolSysMT",
    skip_digestion=False,
    *,
    max_matches=100000,
):
    """Recognizing ordered donor-halogen and acceptor-reference atom pairs.

    Match complete source chemistry before filtering sites by atom selection.
    No coordinates or interaction geometry are inferred by recognition.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form supplying explicit elements, complete connectivity,
        covalent orders, formal charges and atom/bond aromatic flags.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Source atom selection. Retain a site only when both its atoms belong
        to the selection; full-source matching precedes this filter.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) for state resolution and spatial selections.
        Recognition itself does not require coordinates.
    chemical_state : {'reference', 'structure'}, int, or None, default='reference'
        State supplying chemistry. Structure assignments must resolve one state.
    method : str, default='smarts_donor_acceptor'
        ProLIF 2.2.2 ordered chemical SMARTS profile, without geometric criteria.
    assume_complete_connectivity : bool, default=False
        Record an explicit completeness assumption when metadata is insufficient;
        do not repair the chemical graph or infer missing bonds.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate selection.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    max_matches : int, default=100000
        Keyword-only maximum matches per query before selection. Exceeded
        limits raise instead of silently truncating the site inventory.

    Returns
    -------
    dict
        int64 donor_halogen_pairs and acceptor_reference_pairs with shapes
        (n_sites, 2), preserving role order rather than independently sorting
        columns. Empty arrays have shape (0, 2). Metadata contains source and
        selected indices, chemical state, SMARTS, evidence, producer versions
        and detached reference bibliography. Indices are unitless, not IDs.

    Raises
    ------
    ArgumentError
        If the method, selection, state or match limit is invalid.
    StructuralInconsistencyError
        If required chemistry is absent or altered by sanitization.
    UnsupportedHeavyOperationError
        If the query exceeds max_matches.
    MemoryBudgetExceededError
        If chemical matching exceeds its numerical memory estimate.

    Notes
    -----
    The donor is [C,N,Si,F,Cl,Br,I]-[Cl,Br,I,At], excluding F as the terminal
    halogen. Acceptor-reference matches use [N,O,P,S,Se,Te,a;!positive]!#[*]:
    non-triple links, including carbonyl and aromatic links. The acceptor
    definition is intentionally distinct from hydrogen-bond acceptors.
    Each eligible reference neighbor retains its own ordered pair. SMARTS
    sanitization preserves declared chemistry and uses RDKit valence rules.
    Water without indexed bonded atoms has no acceptor-reference match.
    These are candidate sites, not a universal chemical or energy model.

    ProLIF's Apache-2.0 rules are attributed; the ProLIF package is not needed.
    Optional Ackredit credits this recognition, while original geometric-paper
    attribution belongs to the detector that actually evaluates its criterion.

    See Also
    --------
    molsysmt.topology.get_substructure_matches
        Matching arbitrary SMARTS on declared chemical graphs.
    molsysmt.interactions.halogen_bonds.get_halogen_bonds
        Evaluating sparse distance and directional-angle observations.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from rdkit import Chem
    >>> sites = msm.physchem.get_halogen_bond_sites(Chem.MolFromSmiles('CCl.C=O'))
    >>> sites['donor_halogen_pairs'].tolist(), sites['acceptor_reference_pairs'].tolist()
    ([[0, 1]], [[3, 2]])

    .. admonition:: User guide

       See :ref:`Getting halogen-bond sites <Tutorial_Get_halogen_bond_sites>`.

    .. versionadded:: 1.0.0
    """
    import numpy as np

    from molsysmt.physchem._prolif import PROLIF_HALOGEN_PATTERNS, PROLIF_REFERENCE
    from molsysmt.topology import get_substructure_matches

    matches = get_substructure_matches(
        molecular_system,
        PROLIF_HALOGEN_PATTERNS,
        selection=selection,
        structure_indices=structure_indices,
        chemical_state=chemical_state,
        assume_complete_connectivity=assume_complete_connectivity,
        syntax=syntax,
        max_matches=max_matches,
    )
    return dict(
        donor_halogen_pairs=np.unique(matches["matches"][0], axis=0),
        acceptor_reference_pairs=np.unique(matches["matches"][1], axis=0),
        atom_source_indices=matches["source_atom_indices"],
        selected_atom_indices=matches["selection_atom_indices"],
        chemical_state_index=matches["chemical_state_index"],
        method=method,
        method_reference=PROLIF_REFERENCE,
        smarts_patterns=list(PROLIF_HALOGEN_PATTERNS),
        evidence=matches["evidence"],
        software=matches["software"],
        max_matches=max_matches,
        assume_complete_connectivity=assume_complete_connectivity,
        scope="full_source_recognition_then_selection",
    )
