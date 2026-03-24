from .lipid_names import lipid_names

def is_lipid(name):
    """
    Check whether a group name corresponds to a lipid residue.

    Parameters
    ----------
    name : str
        Residue or group name as stored in the topology (e.g. ``'POPC'``,
        ``'DPPC'``).

    Returns
    -------
    bool
        True if ``name`` belongs to the set of known lipid group names, False
        otherwise.

    Notes
    -----
    The recognised names are defined in
    ``molsysmt.element.group.lipid.lipid_names``.

    .. versionadded:: 1.0.0
    """

    return (name in lipid_names)

