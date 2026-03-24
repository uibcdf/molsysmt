from .group_names import group_names

def is_saccharide(name):
    """
    Check whether a group name corresponds to a saccharide (sugar) residue.

    Parameters
    ----------
    name : str
        Residue or group name as stored in the topology (e.g. ``'BGLU'``,
        ``'FUC'``, ``'MAN'``).

    Returns
    -------
    bool
        True if ``name`` belongs to the set of known saccharide group names, False
        otherwise.

    Notes
    -----
    The recognised names are defined in
    ``molsysmt.element.group.saccharide.group_names``.

    .. versionadded:: 1.0.0
    """

    return (name in group_names)

