from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openff.Molecule')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form openff.Molecule.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openff.Molecule
        Resulting object in openff.Molecule form.


    .. versionadded:: 1.0.0
    """

    from copy import deepcopy
    return deepcopy(item)
