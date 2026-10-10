"""Recognizing reusable hydrogen-bond sites without evaluating geometry."""

import numpy as np
from depdigest import dep_digest
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.interaction_attribution import attributed
from molsysmt._private.smonitor import StructuralInconsistencyError


@signal(tags=["api", "interactions", "hbonds"])
@arg_digest()
@dep_digest("rdkit", when={"method": "prolif"})
@dep_digest("rdkit", when={"method": "smarts_donor_acceptor"})
@attributed("hbond_sites")
def get_hbond_sites(
    molecular_system,
    selection="all",
    structure_indices="all",
    chemical_state="reference",
    method="elemental_nitrogen_oxygen",
    assume_complete_connectivity=False,
    syntax="MolSysMT",
    skip_digestion=False,
    *,
    max_matches=100000,
):
    """Recognizing donor-hydrogen pairs and acceptors with an attributed rule.

    This chemical tool does not calculate hydrogen bonds or infer hydrogens
    from coordinates. Every returned hydrogen is an indexed source atom.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form supplying element symbols and complete declared
        covalent connectivity. ProLIF also requires declared formal charges,
        bond orders and atom/bond aromatic flags.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atom selection. Retain donor-hydrogen pairs only when both atoms are
        selected, and acceptors when selected. Match the full source first.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) for state resolution and spatial selections.
        Site recognition itself does not require coordinates.
    chemical_state : {'reference', 'structure'}, int, or None, default='reference'
        State supplying connectivity and chemistry. Structure-assigned states
        must resolve to one state across the requested frames.
    method : str, default='elemental_nitrogen_oxygen'
        elemental_nitrogen_oxygen recognizes N/O donors bonded to indexed H
        and all N/O acceptors; elemental_fluorine_oxygen_nitrogen uses F/O/N
        for both roles. smarts_donor_acceptor uses the attributed ProLIF 2.2.2
        SMARTS. mdtraj, cpptraj and prolif remain compatibility aliases.
    assume_complete_connectivity : bool, default=False
        Explicitly assume supplied connectivity complete when metadata is
        insufficient. The assumption does not change the source chemistry.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate selection.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    max_matches : int, default=100000
        Keyword-only maximum matches per ProLIF SMARTS query, before selection.
        An exceeded limit raises rather than returning a truncated site set.

    Returns
    -------
    dict
        int64 donor_hydrogen_pairs with shape (n_pairs, 2), acceptor_atom_indices
        with shape (n_acceptors,), source atom indices, selected indices, state,
        method reference, chemical evidence and producer versions. No physical
        units apply to these indices. Empty pairs have shape (0, 2).

    Raises
    ------
    ArgumentError
        If the method, selection, state or match limit is invalid.
    StructuralInconsistencyError
        If elements/connectivity or the required declared chemistry are absent.
    UnsupportedHeavyOperationError
        If a ProLIF query exceeds max_matches.

    Notes
    -----
    The returned attribution field contains a detached bibliography, with
    reference implementations distinguished from executed dependencies.
    Optional Ackredit records this completed recognition in the current session.

    These are candidate-site definitions, not universal donor/acceptor chemistry.
    Elemental profiles intentionally include chemically unsuitable N/O atoms;
    they reproduce the reference rules. No water, sidechain, residue or solvent
    pruning is applied. ProLIF SMARTS are reproduced with Apache-2.0 attribution.
    RDKit is optional for that profile; MDTraj, CPPTRAJ and ProLIF packages are
    not production dependencies. Dative links do not create donor-H pairs.

    See Also
    --------
    molsysmt.interactions.hbonds.get_hbonds
        Applying geometric criteria to candidate sites.
    molsysmt.topology.get_substructure_matches
        Matching general chemical SMARTS on declared source graphs.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from rdkit import Chem
    >>> sites = msm.interactions.hbonds.get_hbond_sites(Chem.AddHs(Chem.MolFromSmiles('O')))
    >>> sites['donor_hydrogen_pairs'].tolist(), sites['acceptor_atom_indices'].tolist()
    ([[0, 1], [0, 2]], [0])

    .. admonition:: User guide

       See :ref:`Getting hydrogen-bond sites <Tutorial_Get_hbond_sites>`.

    .. versionadded:: 1.0.0
    """
    from molsysmt import __version__
    from molsysmt._private.scientific_references import (
        CPPTRAJ_REFERENCE,
        MDTRAJ_REFERENCE,
    )
    from molsysmt.basic import get
    from molsysmt.topology._chemical_graph import (
        chemical_graph_context,
        select_chemical_atoms,
    )

    caller = "molsysmt.interactions.hbonds.get_hbond_sites"
    from molsysmt._private.interaction_methods import resolve_method

    method = resolve_method("hbond_sites", method, caller=caller)["implementation"]
    source, states, _, state_index, _, bonds, frames = chemical_graph_context(
        molecular_system,
        chemical_state,
        structure_indices,
        assume_complete_connectivity,
        caller,
    )
    selected = select_chemical_atoms(
        source, states, state_index, selection, frames, syntax
    )
    if method == "prolif":
        from molsysmt.physchem._prolif import PROLIF_HBOND_PATTERNS, PROLIF_REFERENCE
        from molsysmt.topology import get_substructure_matches

        matches = get_substructure_matches(
            source,
            PROLIF_HBOND_PATTERNS,
            chemical_state=state_index,
            assume_complete_connectivity=assume_complete_connectivity,
            max_matches=max_matches,
        )
        pairs = matches["matches"][0].reshape(-1, 2)
        acceptors = matches["matches"][1].ravel()
        reference, software, evidence = (
            PROLIF_REFERENCE,
            matches["software"],
            matches["evidence"],
        )
        patterns = list(PROLIF_HBOND_PATTERNS)
    else:
        from molsysmt.physchem.atoms.mass import physical as elements

        symbols = np.asarray(get(source, element="atom", atom_type=True), dtype=object)
        if symbols.shape != (states.n_atoms,) or any(
            not isinstance(item, str) or item not in elements for item in symbols
        ):
            raise StructuralInconsistencyError(
                reason="An explicit element symbol is required for every atom.",
                caller=caller,
            )
        eligible = np.isin(
            symbols, ["N", "O", "F"] if method == "cpptraj" else ["N", "O"]
        )
        hydrogen = symbols == "H"
        pairs = np.concatenate(
            (
                bonds[eligible[bonds[:, 0]] & hydrogen[bonds[:, 1]]],
                bonds[eligible[bonds[:, 1]] & hydrogen[bonds[:, 0]], ::-1],
            )
        )
        acceptors = np.flatnonzero(eligible)
        reference = CPPTRAJ_REFERENCE if method == "cpptraj" else MDTRAJ_REFERENCE
        software, evidence, patterns = (
            {"molsysmt": __version__},
            "declared_elements_and_covalent_bonds",
            None,
        )
    pairs = np.unique(pairs, axis=0)
    pairs = pairs[np.isin(pairs, selected).all(axis=1)]
    acceptors = np.intersect1d(acceptors, selected)
    return dict(
        donor_hydrogen_pairs=pairs,
        acceptor_atom_indices=acceptors,
        atom_source_indices=np.arange(states.n_atoms, dtype=np.int64),
        selected_atom_indices=selected,
        chemical_state_index=state_index,
        method=method,
        method_reference=reference,
        smarts_patterns=patterns,
        evidence=evidence,
        software=software,
        assume_complete_connectivity=assume_complete_connectivity,
        scope="full_source_recognition_then_selection",
        water_policy="included",
        hydrogen_policy="indexed_atoms_only",
    )
