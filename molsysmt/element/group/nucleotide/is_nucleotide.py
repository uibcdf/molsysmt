from .nucleotide_names import nucleotide_names

def is_nucleotide(name):
    """
    Check whether a group name corresponds to a nucleotide residue.


    Parameters
    ----------
    name : object
        Argument name.

    Returns
    -------
    bool
        True if ``name`` belongs to the set of known nucleotide group names, False
        otherwise.


    Notes
    -----
    The recognised names are defined in
    ``molsysmt.element.group.nucleotide.nucleotide_names`` and cover standard DNA
    and RNA nucleotides.


    .. versionadded:: 1.0.0
    """

    return (name in nucleotide_names)

