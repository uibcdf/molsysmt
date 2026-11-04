from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.MolSys")
def to_string_amino_acids_1(
    item, group_indices="all", skip_digestion=False, *, from_naming_scheme=None
):
    """
    Converting from molsysmt.MolSys to string:amino_acids_1.


    Parameters
    ----------
    item : molecular system
        Argument item.
    group_indices : int, list, tuple, or numpy.ndarray, default='all'
        Source group positions in the requested order, including repetitions.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    from_naming_scheme : str or none, default=None
        Explicit source convention for selected groups: 'sequence', 'amber',
        'ccd' or 'legacy'. None reads stored declarations. Contradictions are
        rejected without modifying the system.

    Returns
    -------
    string:amino_acids_1
        Resulting object in string:amino_acids_1 form.

    Raises
    ------
    ArgumentError
        If topology is absent, group positions are invalid or the requested
        interpretation cannot be resolved consistently.
    ArgumentChoiceError
        If the explicit source convention is unsupported.

    Notes
    -----
    This query reads the existing topology. It neither copies molecular domains
    nor changes names, declarations, chemical states or interaction analyses.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert('amino_acids_3:GlhHid', to_form='molsysmt.MolSys')
    >>> to_string_amino_acids_1(molsys, from_naming_scheme='amber')
    'EH'


    .. versionadded:: 1.0.0
    """

    from molsysmt.form.molsysmt_Topology.to_string_amino_acids_1 import (
        to_string_amino_acids_1 as molsysmt_Topology_to_string_amino_acids_1,
    )

    if item.topology is None:
        from molsysmt._private.smonitor import ArgumentError

        raise ArgumentError(
            "item", caller=__name__, message="Sequence projection requires topology."
        )
    return molsysmt_Topology_to_string_amino_acids_1(
        item.topology,
        group_indices=group_indices,
        from_naming_scheme=from_naming_scheme,
        skip_digestion=True,
    )
