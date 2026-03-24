from .group_names import group_names

def is_ion(name):
    """
    Check whether a group name corresponds to an atomic ion.

    Parameters
    ----------
    name : str
        Residue or group name as stored in the topology (e.g. ``'NA'``, ``'CL'``,
        ``'ZN'``).

    Returns
    -------
    bool
        True if ``name`` belongs to the set of known ion group names, False
        otherwise.

    Notes
    -----
    The recognised names are defined in
    ``molsysmt.element.group.ion.group_names``.

    .. versionadded:: 1.0.0
    """

    return (name in group_names)

