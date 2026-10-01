"""Recognize hydrophobic atoms independently of geometric contact detection."""

from depdigest import dep_digest
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.interaction_attribution import attributed


@signal(tags=["api", "physchem"])
@arg_digest()
@dep_digest("rdkit")
@attributed("hydrophobic_sites")
def get_hydrophobic_sites(
    molecular_system, selection="all", structure_indices="all",
    chemical_state="reference", method="smarts_hydrophobic_atoms",
    assume_complete_connectivity=False, syntax="MolSysMT", skip_digestion=False,
    *, max_matches=100000,
):
    """Recognizing hydrophobic atom sites from complete declared chemical graphs.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form supplying elements, complete connectivity, covalent
        orders, formal charges and atom/bond aromatic flags.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Source atom selection. Recognize the full graph before filtering atoms.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) for state resolution and spatial selections.
        Recognition itself does not require coordinates.
    chemical_state : {'reference', 'structure'}, int, or None, default='reference'
        State supplying chemistry. Structure assignments must resolve one state.
    method : str, default='smarts_hydrophobic_atoms'
        Exact ProLIF 2.2.2 atomic Hydrophobic SMARTS, without geometry.
    assume_complete_connectivity : bool, default=False
        Record an explicit completeness assumption without filling missing bonds
        or chemical assignments.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate selection.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    max_matches : int, default=100000
        Keyword-only maximum full-source matches before selection. Exceeded
        limits raise rather than silently truncating chemical sites.

    Returns
    -------
    dict
        hydrophobic_atom_indices is a sorted int64 array with shape (n_sites,),
        including (0,) when empty. Indices refer to source atoms, not IDs.
        Metadata retains state, source/selected axes, SMARTS, chemical evidence,
        actual producer versions and detached reference bibliography.

    Raises
    ------
    ArgumentError
        If the method, selection, state or match limit is invalid.
    StructuralInconsistencyError
        If required chemistry is absent or altered by sanitization.
    UnsupportedHeavyOperationError
        If a match limit is exceeded.
    MemoryBudgetExceededError
        If chemical matching exceeds its numerical memory estimate.

    Notes
    -----
    This experimental definition reproduces ProLIF 2.2.2, whose patterns are
    adapted from RDKit chemical features. It includes neutral aromatic c/s,
    Br/I, sulfur with no hydrogens and valence two, and specified nonterminal
    aliphatic carbon environments; carbon linked to N/O/F and charged atoms
    are excluded. Terminal methyl carbon is not a blanket match. F and Cl
    themselves do not match. Indexed or annotated hydrogen counts participate
    in RDKit valence interpretation; no hydrogens or coordinates are invented.
    Missing formal-charge/aromatic assignments are not inferred silently.

    Sites are not residue hydrophobicity scale values, interaction energies or
    evidence that an atom universally behaves hydrophobically. ProLIF is a
    reference, not an executed dependency. Optional Ackredit credits completed
    recognition; the bibliography also exists without that provider.

    See Also
    --------
    molsysmt.physchem.get_hydrophobicity
        Looking up independent residue hydrophobicity scales.
    molsysmt.topology.get_substructure_matches
        Matching arbitrary SMARTS on declared chemical graphs.
    molsysmt.interactions.hydrophobic.get_hydrophobic_interactions
        Evaluating typed atom-pair proximity observations.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from rdkit import Chem
    >>> sites = msm.physchem.get_hydrophobic_sites(Chem.MolFromSmiles('CCC.CSC.CF'))
    >>> sites['hydrophobic_atom_indices'].tolist()
    [1, 4]

    .. admonition:: User guide

       See :ref:`Getting hydrophobic sites <Tutorial_Get_hydrophobic_sites>`.

    .. versionadded:: 1.0.0
    """
    import numpy as np

    from molsysmt.physchem._prolif import PROLIF_HYDROPHOBIC_PATTERN, PROLIF_REFERENCE
    from molsysmt.topology import get_substructure_matches

    matches = get_substructure_matches(
        molecular_system, PROLIF_HYDROPHOBIC_PATTERN, selection=selection,
        structure_indices=structure_indices, chemical_state=chemical_state,
        assume_complete_connectivity=assume_complete_connectivity, syntax=syntax,
        max_matches=max_matches,
    )
    return dict(
        hydrophobic_atom_indices=np.unique(matches["matches"][0].ravel()),
        atom_source_indices=matches["source_atom_indices"],
        selected_atom_indices=matches["selection_atom_indices"],
        chemical_state_index=matches["chemical_state_index"], method=method,
        method_reference=PROLIF_REFERENCE, smarts_patterns=[PROLIF_HYDROPHOBIC_PATTERN],
        evidence=matches["evidence"], software=matches["software"], max_matches=max_matches,
        assume_complete_connectivity=assume_complete_connectivity,
        scope="full_source_recognition_then_selection",
    )
