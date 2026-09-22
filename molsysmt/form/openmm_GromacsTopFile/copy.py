from molsysmt._private.argdigest import arg_digest


@arg_digest(form="openmm.GromacsTopFile")
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form openmm.GromacsTopFile.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.GromacsTopFile
        Resulting object in openmm.GromacsTopFile form.


    .. versionadded:: 1.0.0
    """

    from copy import deepcopy

    tmp_item = deepcopy(item)

    return tmp_item
