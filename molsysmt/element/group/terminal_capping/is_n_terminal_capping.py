
def is_n_terminal_capping(name):
    """
    Check whether a group name corresponds to an N-terminal capping residue.

    N-terminal cappings are protecting groups added to the N-terminus of a peptide
    chain (e.g. ``'ACE'`` — acetyl cap).

    Parameters
    ----------
    name : str
        Residue or group name as stored in the topology.

    Returns
    -------
    bool
        True if ``name`` belongs to the set of known N-terminal capping group
        names, False otherwise.

    Notes
    -----
    The recognised names are defined in
    ``molsysmt.element.group.terminal_capping.n_terminal_capping_names``.

    .. versionadded:: 1.0.0
    """
    from . import n_terminal_capping_names
    return (name in n_terminal_capping_names)

