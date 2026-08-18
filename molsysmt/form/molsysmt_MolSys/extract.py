from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='molsysmt.MolSys')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Extracting a subset of elements or structures from form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
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
    molsysmt.MolSys
        Resulting object in molsysmt.MolSys form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.native import MolSys
    if not isinstance(item, MolSys):
        from molsysmt.basic import convert
        item = convert(item, to_form='molsysmt.MolSys', skip_digestion=True)

    return item.extract(atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=copy_if_all,
                        skip_digestion=True)
    
