from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:uniprot_id')
def to_string_uniprot_id(item, atom_indices='all', skip_digestion=False):
    """
    Converting from string:uniprot_id to string:uniprot_id.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:uniprot_id
        Resulting object in string:uniprot_id form.


    .. versionadded:: 1.0.0
    """

    return item
