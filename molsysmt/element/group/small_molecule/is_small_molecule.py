from .group_names import group_names

def is_small_molecule(name):
    """
    Check whether a group name corresponds to a small molecule (ligand or cofactor).

    Parameters
    ----------
    name : str
        Residue or group name as stored in the topology (e.g. ``'ATP'``, ``'HEM'``,
        ``'LIG'``).

    Returns
    -------
    bool
        True if ``name`` belongs to the set of known small-molecule group names,
        False otherwise.

    Notes
    -----
    The recognised names are defined in
    ``molsysmt.element.group.small_molecule.group_names``.

    .. versionadded:: 1.0.0
    """

    return (name in group_names)

