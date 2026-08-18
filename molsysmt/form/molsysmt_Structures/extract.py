from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='molsysmt.Structures')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Extracting a subset of elements or structures from form molsysmt.Structures.

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

    from molsysmt.native import Structures
    if not isinstance(item, Structures):
        from molsysmt.basic import convert
        item = convert(item, to_form='molsysmt.Structures', skip_digestion=True)

    if is_all(atom_indices) and is_all(structure_indices):
        tmp_item = item.copy()
    else:
        tmp_item = item.extract(atom_indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)

    return tmp_item

