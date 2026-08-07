from molsysmt._private.argdigest import arg_digest

@arg_digest()
def has_pbc(molecular_system, skip_digestion=False):
    """
    Check whether a molecular system has periodic boundary conditions (box).

    Parameters
    ----------
    molecular_system : molecular system
        System to inspect.
    skip_digestion : bool, default False
        Whether to skip argument digestion.

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
