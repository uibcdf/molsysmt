from molsysmt._private.argdigest import arg_digest

@arg_digest()
def has_pbc(molecular_system, skip_digestion=False):
    """
    Check whether a molecular system has periodic boundary conditions (box).


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    bool
        `True` if the system has a box defined; otherwise `False`.


    .. versionadded:: 1.0.0
    """

    from molsysmt import get

    box = get(molecular_system, structure_indices=0, box=True, skip_digestion=True)

    output = True

    if box is None:
        output = False

    return output
