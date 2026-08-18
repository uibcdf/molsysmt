from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.Topology')
def to_string_amino_acids_3(item, group_indices='all', skip_digestion=False):
    """
    Converting from molsysmt.Topology to string:amino_acids_3.


    Parameters
    ----------
    item : molecular system
        Argument item.
    group_indices : int, list, tuple, or numpy.ndarray, default='all'
        Argument group_indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:amino_acids_3
        Resulting object in string:amino_acids_3 form.


    .. versionadded:: 1.0.0
    """

    from . import get_group_name_from_group, get_group_type_from_group

    group_names = get_group_name_from_group(item, indices=group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices)
    sequence_group_types = {'amino acid', 'terminal capping'}
    tmp_item = ''.join(
        group_name.title()
        for group_name, group_type in zip(group_names, group_types, strict=True)
        if group_type in sequence_group_types
    )

    return tmp_item
