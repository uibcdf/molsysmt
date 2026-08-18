from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:uniprot_id')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form string:uniprot_id.

    Parameters
    ----------
    item : string:uniprot_id
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    string:uniprot_id
        Copied item.
    """

    return item
