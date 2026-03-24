from .group_names import group_names

def is_terminal_capping(name):
    """
    Check whether a group name corresponds to any terminal capping residue.

    Terminal cappings are protecting groups added to either the N- or C-terminus
    of a peptide chain (e.g. ``'ACE'``, ``'NME'``, ``'NH2'``).

    Parameters
    ----------
    name : str
        Residue or group name as stored in the topology.

    Returns
    -------
    bool
        True if ``name`` belongs to the combined set of known N- and C-terminal
        capping group names, False otherwise.

    Notes
    -----
    The recognised names are defined in
    ``molsysmt.element.group.terminal_capping.group_names``, which is the union of
    ``n_terminal_capping_names`` and ``c_terminal_capping_names``.

    See Also
    --------
    :func:`molsysmt.element.group.terminal_capping.is_n_terminal_capping`
        Check for N-terminal cappings specifically.

    :func:`molsysmt.element.group.terminal_capping.is_c_terminal_capping`
        Check for C-terminal cappings specifically.

    .. versionadded:: 1.0.0
    """
    return (name in group_names)

