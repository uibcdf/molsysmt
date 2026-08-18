from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.Structures')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Converting from molsysmt.Structures to molsysmt.Structures.

    Parameters
    ----------
    item : molsysmt.Structures
        Source item in molsysmt.Structures form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    copy_if_all : object
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Structures
        Resulting object in molsysmt.Structures form.

    .. versionadded:: 1.0.0
    """

    from .extract import extract

    return extract(item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=copy_if_all, skip_digestion=True)

