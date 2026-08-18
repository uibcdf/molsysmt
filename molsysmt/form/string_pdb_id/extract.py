from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='string:pdb_id')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Extracting a subset of atoms or structures from form string:pdb_id.

    Parameters
    ----------
    item : string:pdb_id
        Source item.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atom selection to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices to extract.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    string:pdb_id
        Extracted subset in the same form.
    """

    if is_all(atom_indices) and is_all(structure_indices):

        raise NotImplementedMethodError()

    else:

        raise NotImplementedMethodError()

    return tmp_item

