def is_n_terminal_capping(name):
    """
    Checking whether a group name identifies an N-terminal peptide cap.

    N-terminal cappings are protecting groups added to the N-terminus of a peptide
    chain (e.g. ``'ACE'`` — acetyl cap).


    Parameters
    ----------
    name : str
        Case-sensitive group label to check. Unsupported labels return False.

    Returns
    -------
    bool
        True if ``name`` belongs to the set of known N-terminal capping group
        names, False otherwise.


    Notes
    -----
    The recognised names are defined in
    ``molsysmt.element.group.terminal_capping.n_terminal_capping_names``.
    N-terminal describes the peptide end being protected, not the cap's
    connecting atom: ACE supplies a carbonyl C bonded to the peptide N.

    Examples
    --------
    >>> is_n_terminal_capping('ACE')
    True
    >>> is_n_terminal_capping('NME')
    False


    .. versionadded:: 1.0.0
    """
    from . import n_terminal_capping_names

    return name in n_terminal_capping_names
