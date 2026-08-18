from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:uniprot_id')
def to_string_uniprot_id(item, atom_indices='all', skip_digestion=False):
    """
    Converting from string:uniprot_id to string.uniprot.id.

    Parameters
    ----------
    item : string:uniprot_id
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    string.uniprot.id
        Converted molecular system representation.
    """

    return item
