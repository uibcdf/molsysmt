from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.Topology")
def to_string_amino_acids_1(item, group_indices="all", skip_digestion=False):
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

    Returns
    -------
    string:amino_acids_1
        Resulting object in string:amino_acids_1 form.

    Notes
    -----
    Stored group-name conventions are read per selected group. Context-dependent
    or unassessed names without a declaration are rejected; no global Amber,
    CCD or legacy fallback is selected. Non-amino-acid groups are omitted.
    Projection preserves names and chemical assignments. Optional Ackredit
    credit is collected once for the complete query, not per group.


    .. versionadded:: 1.0.0
    """

    from molsysmt._private.name_resolution import native_sequence

    return native_sequence(item, group_indices, caller=__name__)
