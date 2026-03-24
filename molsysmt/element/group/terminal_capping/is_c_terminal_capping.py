
def is_c_terminal_capping(name):
    """
    Check whether a group name corresponds to a C-terminal capping residue.

    C-terminal cappings are protecting groups added to the C-terminus of a peptide
    chain (e.g. ``'NME'`` — N-methyl amide, ``'NH2'`` — amide).

    Parameters
    ----------
    name : str
        Residue or group name as stored in the topology.

    Returns
    -------
    bool
        True if ``name`` belongs to the set of known C-terminal capping group
        names, False otherwise.

    Notes
    -----
    The recognised names are defined in
    ``molsysmt.element.group.terminal_capping.c_terminal_capping_names``.

    .. versionadded:: 1.0.0
    """
    from . import c_terminal_capping_names
    return (name in c_terminal_capping_names)

