from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:smiles')
def to_string_smiles(item, skip_digestion=False):
    """
    Converting from string:smiles to string.smiles.

    Parameters
    ----------
    item : string:smiles
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    string.smiles
        Converted molecular system representation.
    """

    from copy import copy
    return copy(item)
