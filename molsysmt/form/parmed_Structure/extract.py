from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from depdigest import dep_digest

@arg_digest(form='parmed.Structure')
@dep_digest('parmed')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Extracting a subset of elements or structures from form parmed.Structure.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    copy_if_all : object, default=True
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    parmed.Structure
        Resulting object in parmed.Structure form.


    .. versionadded:: 1.0.0
    """

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all:
            from copy import deepcopy
            tmp_item = deepcopy(item)
        else:
            tmp_item = item
    else:
        from copy import deepcopy

        tmp_item = deepcopy(item)
        if not is_all(atom_indices):
            from molsysmt._private.atom_indices import atom_indices_to_AmberMask
            from molsysmt._private.atom_indices import complementary_atom_indices

            removed_atom_indices = complementary_atom_indices(item, atom_indices)
            mask = atom_indices_to_AmberMask(item, removed_atom_indices)
            tmp_item.strip(mask)
        if not is_all(structure_indices) and tmp_item.coordinates is not None:
            tmp_item.coordinates = tmp_item.get_coordinates('all')[structure_indices]

    return tmp_item
