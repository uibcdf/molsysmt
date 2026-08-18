from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openff.Molecule')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form openff.Molecule.

    Parameters
    ----------
    item : openff.Molecule
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openff.Molecule
        Copied item.
    """

    from copy import deepcopy
    return deepcopy(item)
