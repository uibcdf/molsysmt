from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.Topology")
def to_string_amino_acids_1(
    item, group_indices="all", skip_digestion=False, *, from_naming_scheme=None
):
    """
    Converting from molsysmt.Topology to string:amino_acids_1.


    Parameters
    ----------
    item : molecular system
        Argument item.
    group_indices : int, list, tuple, or numpy.ndarray, default='all'
        Positional source groups to project, preserving order and repetitions.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    from_naming_scheme : str or none, default=None
        Explicit source convention for selected groups: 'sequence', 'amber',
        'ccd' or 'legacy'. None reads stored declarations. An explicit convention
        must agree with every known selected declaration; the source is unchanged.

    Returns
    -------
    string:amino_acids_1
        Resulting object in string:amino_acids_1 form.

    Raises
    ------
    ArgumentError
        If group positions are invalid, required context is absent, the source
        convention contradicts stored declarations or a name has no projection.
    ArgumentChoiceError
        If the explicit source convention is unsupported.

    Notes
    -----
    Stored group-name conventions are read per selected group. Context-dependent
    or unassessed names without a declaration are rejected; no global Amber,
    CCD or legacy fallback is selected. Non-amino-acid groups are omitted.
    Projection preserves names and chemical assignments. Optional Ackredit
    credit is collected once for the complete query, not per group.

    Examples
    --------
    >>> import molsysmt as msm
    >>> topology = msm.convert('amino_acids_3:GlhHid', to_form='molsysmt.Topology')
    >>> to_string_amino_acids_1(topology, from_naming_scheme='amber')
    'EH'
    >>> topology.group_naming_schemes
    (None, None)


    .. versionadded:: 1.0.0
    """

    from molsysmt._private.name_resolution import native_sequence

    return native_sequence(
        item, group_indices, caller=__name__, from_naming_scheme=from_naming_scheme
    )
