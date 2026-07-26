from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='XYZ')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    import numpy as np
    from molsysmt.native.structures import Structures
    from molsysmt._private.variables import is_all
    from . import get_coordinates_from_atom

    tmp_item = Structures()
    if not is_all(atom_indices):
        atom_indices = np.sort(np.asarray(atom_indices, dtype=int))
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices,
                                            skip_digestion=True)
    tmp_item.append(coordinates=coordinates, skip_digestion=True)

    return tmp_item
