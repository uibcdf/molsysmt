"""Recognize chemical metal and ligand sites independently of observed geometry."""

from depdigest import dep_digest
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.interaction_attribution import attributed


@signal(tags=["api", "physchem"])
@arg_digest()
@dep_digest("rdkit")
@attributed("metal_coordination_sites")
def get_metal_coordination_sites(
    molecular_system,
    selection="all",
    structure_indices="all",
    chemical_state="reference",
    method="smarts_metal_ligand",
    assume_complete_connectivity=False,
    syntax="MolSysMT",
    skip_digestion=False,
    *,
    max_matches=100000,
):
    """Recognizing metal and candidate ligand atoms from declared chemical graphs.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form supplying elements, complete connectivity, covalent
        orders, formal charges and atom/bond aromatic flags.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Source atom selection. Recognize full chemistry before filtering atoms.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) for state resolution and spatial selections.
        Recognition does not require coordinates.
    chemical_state : {'reference', 'structure'}, int, or None, default='reference'
        State supplying chemistry. Structure assignments must resolve one state.
    method : str, default='smarts_metal_ligand'
        Exact ProLIF 2.2.2 MetalDonor metal and ligand SMARTS, without geometry.
    assume_complete_connectivity : bool, default=False
        Record a completeness assumption without repairing chemical assignments.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate selection.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    max_matches : int, default=100000
        Keyword-only maximum full-source matches per SMARTS before selection.
        Exceeded limits raise rather than truncate sites.

    Returns
    -------
    dict
        Sorted int64 metal_atom_indices and ligand_atom_indices, each shape
        (n_sites,), plus source/selected axes, state, patterns, chemical evidence,
        reference bibliography and actual producer versions. Empty arrays use (0,).

    Raises
    ------
    ArgumentError
        If method, selection, state or match limit is invalid.
    StructuralInconsistencyError
        If chemistry is missing or sanitization would change assignments.
    UnsupportedHeavyOperationError
        If chemical matching exceeds max_matches.
    MemoryBudgetExceededError
        If numerical chemical matching exceeds its working estimate.

    Notes
    -----
    The reference metal set is Ca, Cd, Co, Cu, Fe, Mg, Mn, Ni and Zn. It is a
    bounded profile, not all metals. Ligands include O, chemically restricted
    N, and negative nonpositive atoms; protonated/quaternary and selected
    conjugated nitrogens are excluded. A negative atom can be both a metal
    and a ligand site. Keep those roles distinct; geometry excludes self pairs.
    Covalent graph matching excludes dative links. These sites are not evidence
    of oxidation state, coordination number, affinity or a declared bond.
    ProLIF is a reference implementation, not an executed dependency.

    See Also
    --------
    molsysmt.topology.get_substructure_matches
        Matching general SMARTS on complete declared chemical graphs.
    molsysmt.interactions.metal_coordination.get_metal_coordination
        Observing sparse metal-ligand proximity candidates.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from rdkit import Chem
    >>> sites = msm.physchem.get_metal_coordination_sites(Chem.MolFromSmiles('[Zn+2].O'))
    >>> sites['metal_atom_indices'].tolist(), sites['ligand_atom_indices'].tolist()
    ([0], [1])

    .. admonition:: User guide

       See :ref:`Getting metal coordination sites <Tutorial_Get_metal_coordination_sites>`.

    .. versionadded:: 1.0.0
    """
    import numpy as np

    from molsysmt.physchem._prolif import PROLIF_METAL_PATTERNS, PROLIF_REFERENCE
    from molsysmt.topology import get_substructure_matches

    matches = get_substructure_matches(
        molecular_system,
        PROLIF_METAL_PATTERNS,
        selection=selection,
        structure_indices=structure_indices,
        chemical_state=chemical_state,
        assume_complete_connectivity=assume_complete_connectivity,
        syntax=syntax,
        max_matches=max_matches,
    )
    return dict(
        metal_atom_indices=np.unique(matches["matches"][0].ravel()),
        ligand_atom_indices=np.unique(matches["matches"][1].ravel()),
        atom_source_indices=matches["source_atom_indices"],
        selected_atom_indices=matches["selection_atom_indices"],
        chemical_state_index=matches["chemical_state_index"],
        method=method,
        method_reference=dict(PROLIF_REFERENCE),
        smarts_patterns=list(PROLIF_METAL_PATTERNS),
        evidence=matches["evidence"],
        software=matches["software"],
        max_matches=max_matches,
        assume_complete_connectivity=assume_complete_connectivity,
        scope="full_source_recognition_then_selection",
    )
