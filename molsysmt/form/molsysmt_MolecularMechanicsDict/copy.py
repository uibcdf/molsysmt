from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.MolecularMechanicsDict")
def copy(item, skip_digestion=False):
    """
    Copying a mechanical parameter dictionary independently.


    Parameters
    ----------
    item : molecular system
        Mechanical parameter dictionary. Nested lists, numeric arrays and
        quantities are detached while preserving their units and values.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolecularMechanicsDict
        Resulting object in molsysmt.MolecularMechanicsDict form.


    .. versionadded:: 1.0.0
    """

    from copy import deepcopy

    return deepcopy(item)
