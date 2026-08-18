from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='molsysmt.MolSys')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Extracting a subset of atoms or structures from form molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atom selection to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices to extract.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.MolSys
        Extracted subset in the same form.
    """

    from molsysmt.native import MolSys
    if not isinstance(item, MolSys):
        from molsysmt.basic import convert
        item = convert(item, to_form='molsysmt.MolSys', skip_digestion=True)

    return item.extract(atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=copy_if_all,
                        skip_digestion=True)
    
