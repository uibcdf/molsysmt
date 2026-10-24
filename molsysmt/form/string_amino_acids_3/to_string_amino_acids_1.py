from molsysmt._private.argdigest import arg_digest


@arg_digest(form="string:amino_acids_3")
def to_string_amino_acids_1(item, group_indices="all", skip_digestion=False):
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

    Returns
    -------
    string:amino_acids_1
        Resulting object in string:amino_acids_1 form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.element.group.amino_acid import get_1_letter_code_from_name
    from molsysmt.element.group.terminal_capping import group_names as caps

    from .extract import extract

    selected = extract(item, group_indices=group_indices, skip_digestion=True)
    sequence = selected.removeprefix("amino_acids_3:")
    groups = [
        sequence[index : index + 3].upper() for index in range(0, len(sequence), 3)
    ]
    letters = "".join(
        get_1_letter_code_from_name(group) for group in groups if group not in caps
    )
    return letters if letters else "amino_acids_1:"
