from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, check=True):

    if check:

        digest_item(item, 'molsysmt.TrajectoryDict')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)


    if (atom_indices is 'all') and (structure_indices is 'all'):

        if copy_if_all:
            from copy import deepcopy
            tmp_item = deepcopy(item)
        else:
            tmp_item = item
    else:

        raise NotImplementedError()

    return tmp_item

