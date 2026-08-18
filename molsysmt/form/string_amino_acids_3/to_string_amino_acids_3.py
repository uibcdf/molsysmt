from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:amino_acids_3')
def to_string_amino_acids_3(item, group_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Converting from string:amino_acids_3 to string.amino.acids.3.

    Parameters
    ----------
    item : string:amino_acids_3
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    string.amino.acids.3
        Converted molecular system representation.
    """

    from .extract import extract

    return extract(item, group_indices=group_indices, copy_if_all=copy_if_all, skip_digestion=True)

