"""Recognize complete explicitly indexed neutral water molecules."""

from depdigest import dep_digest
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.interaction_attribution import attributed


@signal(tags=["api", "physchem"])
@arg_digest()
@dep_digest("rdkit")
@attributed("water_sites")
def get_water_sites(
    molecular_system,
    selection="all",
    structure_indices="all",
    chemical_state="reference",
    method="explicit_water_graph",
    assume_complete_connectivity=False,
    syntax="MolSysMT",
    skip_digestion=False,
    *,
    max_matches=100000,
):
    """Recognizing neutral water molecules with three explicitly indexed atoms.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form supplying elements, complete connectivity, covalent
        orders, formal charges and atom/bond aromatic flags.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Source atom selection. Retain water only when all three atoms belong to
        the selection. Recognize the full chemical graph before filtering.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) for state resolution and spatial selections.
        Recognition itself does not require coordinates.
    chemical_state : {'reference', 'structure'}, int, or None, default='reference'
        State supplying chemistry. Structure assignments must resolve one state.
    method : str, default='explicit_water_graph'
        Neutral O with exactly two single-bonded, degree-one neutral indexed H.
    assume_complete_connectivity : bool, default=False
        Record a completeness assumption without repairing chemical assignments.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate selection.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    max_matches : int, default=100000
        Keyword-only maximum full-source SMARTS matches before selection.
        Exceeded limits raise rather than silently truncating water molecules.

    Returns
    -------
    dict
        int64 water_atom_indices with shape (n_waters, 3), ordered oxygen then
        ascending hydrogen indices, plus source/selected axes, chemical state,
        recognition evidence, actual producer versions and bibliography. Empty
        water_atom_indices has shape (0, 3).

    Raises
    ------
    ArgumentError
        If method, selection, state or match limit is invalid.
    StructuralInconsistencyError
        If required chemistry is absent or altered by sanitization.
    UnsupportedHeavyOperationError
        If chemical matching exceeds max_matches.
    MemoryBudgetExceededError
        If numerical chemical matching exceeds its working estimate.

    Notes
    -----
    Recognize the explicit molecular graph rather than a water residue name.
    Oxygen-only water with implicit hydrogens, hydroxide, hydronium, alcohols,
    peroxide and covalently shared hydrogens are excluded. Isotopic hydrogen
    remains an indexed H. No hydrogens or coordinates are added. Dative links
    are independent of the covalent graph, so metal-coordinated water remains
    eligible. Virtual-site water models with additional covalent sites need a
    separately specified recognition profile. This definition does not certify
    a force-field water model or hydrogen-bond donor/acceptor rule.

    See Also
    --------
    molsysmt.physchem.get_hbond_sites
        Recognizing hydrogen-bond roles independently of water identity.
    molsysmt.interactions.water_bridges.get_water_bridges
        Composing single-water paths from two observed hydrogen bonds.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from rdkit import Chem
    >>> sites = msm.physchem.get_water_sites(Chem.AddHs(Chem.MolFromSmiles('O.CO')))
    >>> sites['water_atom_indices'].tolist()
    [[0, 3, 4]]

    .. admonition:: User guide

       See :ref:`Getting water sites <Tutorial_Get_water_sites>`.

    .. versionadded:: 1.0.0
    """
    import numpy as np

    from molsysmt.topology import get_substructure_matches

    pattern = "[O;+0;D2;H2](-[#1;+0;D1])-[#1;+0;D1]"
    matches = get_substructure_matches(
        molecular_system,
        pattern,
        selection=selection,
        structure_indices=structure_indices,
        chemical_state=chemical_state,
        assume_complete_connectivity=assume_complete_connectivity,
        syntax=syntax,
        max_matches=max_matches,
    )
    waters = matches["matches"][0].copy().reshape(-1, 3)
    waters[:, 1:] = np.sort(waters[:, 1:], axis=1)
    waters = np.unique(waters, axis=0)
    return dict(
        water_atom_indices=waters,
        atom_source_indices=matches["source_atom_indices"],
        selected_atom_indices=matches["selection_atom_indices"],
        chemical_state_index=matches["chemical_state_index"],
        method=method,
        smarts_patterns=[pattern],
        evidence=matches["evidence"],
        software=matches["software"],
        max_matches=max_matches,
        assume_complete_connectivity=assume_complete_connectivity,
        scope="full_source_recognition_then_selection",
        hydrogen_policy="indexed_atoms_only",
    )
