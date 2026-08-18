from .group_names import group_names

def is_amino_acid(name):
    """
    Check whether a group name corresponds to an amino acid residue.


    Parameters
    ----------
    name : object
        Argument name.

    Returns
    -------
    bool
        True if ``name`` belongs to the set of known amino acid group names,
        False otherwise.


    Notes
    -----
    The recognised names are defined in
    ``molsysmt.element.group.amino_acid.group_names``.


    .. versionadded:: 1.0.0
    """

    output = (name in group_names)

    return (name in group_names)

