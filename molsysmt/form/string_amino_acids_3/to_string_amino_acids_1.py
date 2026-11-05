from molsysmt._private.argdigest import arg_digest


@arg_digest(form="string:amino_acids_3")
def to_string_amino_acids_1(
    item, group_indices="all", skip_digestion=False, *, from_naming_scheme=None
):
    """
    Converting from string:amino_acids_3 to string:amino_acids_1.


    Parameters
    ----------
    item : molecular system
        Sequence text in the declared alphabet; an explicit amino_acids prefix is supported.
    group_indices : int, list, tuple, or numpy.ndarray, default='all'
        Original sequence-group positions; terminal caps are omitted after selection.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    from_naming_scheme : str or none, default=None
        Explicit source vocabulary: 'sequence', 'amber', 'ccd' or 'legacy'.
        None admits the sequence alphabet and assessed unambiguous modified
        projections; context-dependent labels require a convention.

    Returns
    -------
    string:amino_acids_1
        Resulting object in string:amino_acids_1 form.

    Raises
    ------
    ArgumentError
        If codes are malformed, group positions are invalid, naming context is
        required or the declared component has no amino-acid projection.
    ArgumentChoiceError
        If the source convention is unsupported.

    Notes
    -----
    Canonical codes use the sequence alphabet. Other names use only assessed
    unambiguous meanings unless a source convention is supplied; there is no
    implicit legacy fallback. Terminal caps are omitted after selection. This
    projection does not modify the input, choose a chemical state or replace a
    modified group. Optional Ackredit credits reached data once per query.

    Examples
    --------
    >>> to_string_amino_acids_1('AceAlaGlyNme')
    'AG'
    >>> to_string_amino_acids_1('GlhHid', from_naming_scheme='amber')
    'EH'

    .. admonition:: User guide

       See :ref:`user-foundations-group-naming-schemes` and
       :ref:`Tutorial_Form_string_amino_acids_3`.

    .. versionadded:: 1.0.0
    """

    from molsysmt._private.name_resolution import project_sequence
    from molsysmt.element.group.amino_acid.codes import aa3_to_aa1
    from molsysmt.element.group.terminal_capping import group_names as caps
    from molsysmt.form._sequence_topology import group_names

    from .extract import extract

    group_names(item.removeprefix("amino_acids_3:"), 3, caller=__name__)
    selected = extract(item, group_indices=group_indices, skip_digestion=True)
    sequence = selected.removeprefix("amino_acids_3:")
    groups = [
        sequence[index : index + 3].upper() for index in range(0, len(sequence), 3)
    ]
    letters, _ = project_sequence(
        groups,
        ("terminal capping" if name in caps else "amino acid" for name in groups),
        range(len(groups)),
        (
            from_naming_scheme
            if from_naming_scheme is not None
            else "sequence"
            if name in aa3_to_aa1
            else None
            for name in groups
        ),
        caller=__name__,
    )
    return letters if letters else "amino_acids_1:"
