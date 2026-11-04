def is_c_terminal_capping(name):
    """
    Checking whether a group name identifies a C-terminal peptide cap.

    C-terminal cappings are protecting groups added to the C-terminus of a peptide
    chain (e.g. ``'NME'`` — N-methyl amide, ``'NH2'`` — amide).


    Parameters
    ----------
    name : str
        Case-sensitive group label to check. Unsupported labels return False.

    Returns
    -------
    bool
        True if ``name`` belongs to the set of known C-terminal capping group
        names, False otherwise.


    Notes
    -----
    The recognised names are defined in
    ``molsysmt.element.group.terminal_capping.c_terminal_capping_names``.
    C-terminal describes the peptide end being protected, not the cap's
    connecting atom: NME, NHE and NH2 supply N bonded to the peptide carbonyl C.

    Examples
    --------
    >>> is_c_terminal_capping('NME')
    True
    >>> is_c_terminal_capping('ACE')
    False


    .. versionadded:: 1.0.0
    """
    from . import c_terminal_capping_names

    return name in c_terminal_capping_names
