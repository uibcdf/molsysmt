from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from depdigest import dep_digest

@arg_digest(form='parmed.Structure')
@dep_digest('parmed')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

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
