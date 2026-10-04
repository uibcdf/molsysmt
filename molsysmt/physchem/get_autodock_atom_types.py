"""Assigning a named AutoDock label profile independently of docking protocols."""

from depdigest import dep_digest
from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "physchem"])
@arg_digest()
@dep_digest("rdkit")
def get_autodock_atom_types(
    molecular_system,
    typing_scheme,
    selection="all",
    structure_indices="all",
    chemical_state="reference",
    method="chemical_environment",
    return_report=False,
    syntax="MolSysMT",
    skip_digestion=False,
):
    """Getting full-graph chemical AutoDock labels before filtering source atoms.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form supplying a complete closed-shell covalent graph,
        elements, formal charges and supported bond orders. All H must be indexed.
        Missing aromaticity is perceived on a detached graph; known conflicts fail.
    typing_scheme : str
        Required explicit 'autodock4' label vocabulary. Labels remain separate
        from MolSysMT atom_type, which denotes chemical element symbols.
    selection : str, list, tuple or numpy.ndarray, default='all'
        Atoms to return, after full-source classification. Indices are sorted
        and deduplicated; selected fragments are not classified in isolation.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Structure indices (0-based) for state resolution and spatial selection.
        Chemical typing itself does not use coordinates.
    chemical_state : str or int, default='reference'
        Selected state; 'structure' must resolve unambiguously across frames.
    method : str, default='chemical_environment'
        Experimental chemical_environment@1 profile, using element, explicit
        aromatic perception, valence, adjacency and formal charge. Later specific
        rules override defaults; no atom/residue name heuristic is used.
    return_report : bool, default=False
        Return atom_ff_type and detached auditable report when True.
    syntax : str, default='MolSysMT'
        Syntax used for atom selection.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    numpy.ndarray or dict
        U2 atom_ff_type labels with shape (n_selected_atoms,), including (0,).
        The optional report contains source indices, full evaluated scope, state,
        scheme/version, original software, ordered rules, per-atom winner codes,
        overlap counts and separate polar/nonpolar H indices. Indices and labels
        have no physical units. The source is unchanged.

    Raises
    ------
    ArgumentError
        If the scheme, method, state, selection or frame request is invalid.
    StructuralInconsistencyError
        If chemistry is incomplete/contradictory, H are virtual, an element or
        charge environment has no qualified rule, or perception fails.
    ImportError
        If the required optional RDKit provider is unavailable.

    Notes
    -----
    The bounded profile supports H/C/N/O/F/P/S/Cl/Br/I with documented formal
    charge environments. It distinguishes aromatic C, trivalent conjugated N,
    positive N, two-connected nonaromatic S and H bonded to N/O/F/P/S.
    These AutoDock labels are a parameter profile, not universal donor/acceptor
    chemistry. See the User Guide for exact precedence and exclusions.
    Meeko 0.8.0 was a source reference; no Meeko code/table is vendored and it is
    not an installed dependency. Metal/pseudoatom/macrocycle typing, partial
    charges, protonation and H merging are outside this operation. RDKit performs
    explicit aromatic perception; optional Ackredit failures preserve results.

    See Also
    --------
    molsysmt.build.assign_autodock_atom_types : Attach a full named type assignment.
    molsysmt.physchem.get_aromaticity : Perceive the reusable aromatic model.
    molsysmt.element.atom.get_atom_type_from_atom_ff_type : Decode existing labels.

    Examples
    --------
    >>> import molsysmt as msm
    >>> result = msm.physchem.get_autodock_atom_types(
    ...     msm.systems['caffeine']['caffeine.sdf'], typing_scheme='autodock4')
    >>> result.shape, result.dtype.name
    ((24,), 'str64')

    .. admonition:: User guide

       See :ref:`Tutorial_AutoDock_Typing` for rules, provenance and limitations.

    .. versionadded:: 1.0.0
    """
    if not isinstance(skip_digestion, bool):
        from molsysmt._private.argdigest.argument.skip_digestion import (
            digest_skip_digestion,
        )

        digest_skip_digestion(
            skip_digestion, caller=__name__ + ".get_autodock_atom_types"
        )
    from molsysmt._private.autodock_assignment import calculate

    result = calculate(
        molecular_system,
        typing_scheme,
        method,
        selection,
        structure_indices,
        chemical_state,
        syntax,
    )
    return result if return_report else result["atom_ff_type"]
