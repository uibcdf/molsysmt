from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:amino_acids_3')
def to_string_amino_acids_3(item, group_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Converting from string:amino_acids_3 to string:amino_acids_3.

    Parameters
    ----------
    item : string:amino_acids_3
        Source item in string:amino_acids_3 form.
    group_indices : str, list, tuple, or numpy.ndarray, default='all'
        Group indices (0-based) to include.
    copy_if_all : object
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:amino_acids_3
        Resulting object in string:amino_acids_3 form.

    .. versionadded:: 1.0.0
    """

    from .extract import extract

    return extract(item, group_indices=group_indices, copy_if_all=copy_if_all, skip_digestion=True)

