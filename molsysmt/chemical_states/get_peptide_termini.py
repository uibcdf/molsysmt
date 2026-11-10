"""Recognizing peptide ends from stored named backbone connectivity."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "chemical_states"])
@arg_digest()
def get_peptide_termini(
    molecular_system,
    selection="all",
    syntax="MolSysMT",
    *,
    chemical_state="reference",
    structure_indices="all",
    on_ambiguous="raise",
    skip_digestion=False,
):
    """Recognizing free and capped ends of stored peptide backbones.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form providing stable atom/group/chain context and stored
        chemical connectivity. Topology alone does not supply bonds.
    selection : str, list, tuple or numpy.ndarray, default='all'
        Source atom selection. Complete chains containing selected amino-acid
        groups are examined before filtering the returned endpoint arrays.
        Selecting an internal group does not create a chemical terminus.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate selection.
    chemical_state : str, int or None, default='reference'
        Stored state supplying bonds. 'structure' requires one associated state
        across the requested structures. The reference is never changed.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Source structure indices used for state association and spatial queries.
        Geometry is not used to infer peptide bonds or termini.
    on_ambiguous : {'raise', 'report'}, default='raise'
        Raise on an ambiguous backbone, or explicitly retain an unassessed
        chain row with its reason and no endpoints. Invalid source axes and
        unknown chain membership are always errors. Report mode emits no warning.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for already validated inputs.

    Returns
    -------
    dict
        Detached report with int64 n_terminal_group_indices and
        c_terminal_group_indices for selected free endpoints; corresponding
        n_capped_group_indices and c_capped_group_indices; selected atom indices,
        chemical_state_index, method, evidence and software. Each chains record
        retains chain_index, ordered amino-acid group_indices, cyclic and cap
        flags, status/reason, and endpoint group indices (None for a cycle or
        unassessed chain). Unassessed populations have no inferred order; their
        group indices are sorted source positions. Empty index arrays
        have shape (0,). Endpoint arrays use source group positions, never IDs.

    Raises
    ------
    StructuralInconsistencyError
        If chemical/stable context is absent, chain membership is unknown,
        backbone atoms or links are ambiguous, or a selected chain contains
        disconnected or branched named backbones. Unsupported end attachments
        are refused rather than interpreted as free termini.
    ArgumentError
        If a selection, structure scope or chemical-state request is invalid.

    Notes
    -----
    This experimental recognizer follows stored N-CA-C motifs and inter-group
    C-N links. Each selected chain must contain one connected linear path or
    cycle covering its amino-acid groups. ACE and NME/NHE/NH2 attachments are
    recognized by their named connecting atoms and stored bonds, not inventory
    adjacency. Non-backbone crosslinks such as S-S do not order a peptide.
    Explicit dative bonds are excluded; legacy untyped stored bonds remain
    admitted and their counts are recorded. Bond order, valence, protonation,
    stereochemistry and global connectivity completeness are not certified.

    A missing link in a declared chain is ambiguous and is refused; no sequence
    order, chain break, new bond or missing chemistry is inferred from atom/group
    positions, group IDs or coordinates. A cycle has no free endpoints.
    Numeric/all modular H5MSM input reads chemistry without its structural series
    or saved interaction analyses. Rich spatial selections can require coordinates.
    The report does not modify inventory, chemical states or coordinates.
    Explicit report mode retains ambiguous chains without contributing endpoints;
    it never treats each disconnected fragment as a separate free peptide.

    See Also
    --------
    molsysmt.chemical_states.get_covalent_paths
        Querying general ordered patterns in a stored bond graph.
    molsysmt.build.get_missing_terminal_cappings
        Reporting missing OXT at recognized free carboxyl termini.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.build.build_peptide('AlaValPro', engine='MolSysMT')
    >>> ends = msm.chemical_states.get_peptide_termini(molsys)
    >>> ends['n_terminal_group_indices'].tolist()
    [0]
    >>> ends['c_terminal_group_indices'].tolist()
    [2]

    .. admonition:: User guide

       See :ref:`Tutorial_Get_peptide_termini` for scope and refusals.

    .. versionadded:: 1.0.0
    """
    from ._peptide_termini import recognize

    return recognize(
        molecular_system,
        selection,
        syntax,
        chemical_state,
        structure_indices,
        on_ambiguous,
    )
