from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:amino_acids_3')
def to_string_amino_acids_1(item, group_indices='all', skip_digestion=False):
    """
    Converting from string:amino_acids_3 to string:amino_acids_1.

    Parameters
    ----------
    item : string:amino_acids_3
        Source item in string:amino_acids_3 form.
    group_indices : str, list, tuple, or numpy.ndarray, default='all'
        Group indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:amino_acids_1
        Resulting object in string:amino_acids_1 form.

    .. versionadded:: 1.0.0
    """

    if item.startswith('amino_acids_3:'):
        item = item[12:]

    from molsysmt.element.group.amino_acid import get_1_letter_code_from_name
    from molsysmt.element.group.terminal_capping import group_names as terminal_capping_names

    tmp_item = ''

    chunks = [item[ii:ii+3].upper() for ii in range(0, len(item), 3)]

    for chunk in chunks:
        if chunk not in terminal_capping_names:
            tmp_item += get_1_letter_code_from_name(chunk)

    return tmp_item

