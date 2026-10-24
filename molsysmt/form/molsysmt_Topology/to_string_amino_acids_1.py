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
        Argument group_indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:amino_acids_1
        Resulting object in string:amino_acids_1 form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.topology._sequence import amino_acid_groups

    from . import get_group_name_from_group, get_group_type_from_group

    names = get_group_name_from_group(item, indices=group_indices)
    types = get_group_type_from_group(item, indices=group_indices)
    sequence, _ = amino_acid_groups(names, types, range(len(names)))
    return sequence
