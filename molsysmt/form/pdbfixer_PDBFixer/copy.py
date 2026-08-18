from molsysmt._private.argdigest import arg_digest

@arg_digest(form='pdbfixer.PDBFixer')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form pdbfixer.PDBFixer.

    Parameters
    ----------
    item : pdbfixer.PDBFixer
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    pdbfixer.PDBFixer
        Copied item.
    """

    from copy import deepcopy
    tmp_item = deepcopy(item)

    return tmp_item
