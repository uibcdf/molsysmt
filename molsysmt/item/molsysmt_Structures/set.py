from molsysmt._private.digestion import digest_item as _digest_item
from molsysmt._private.digestion import digest_indices as _digest_indices
from molsysmt._private.digestion import digest_structure_indices as _digest_structure_indices

###### Set

## System

def set_box_to_system(item, indices='all', structure_indices='all', value=None):

    if check:

        _digest_item(item, 'molsysmt.Structures')
        indices = _digest_indices(indices)
        structure_indices = _digest_structure_indices(structure_indices)

    n_structures_trajectory = item.coordinates.shape[0]
    n_structures_box = value.shape[0]

    if n_structures_trajectory == n_structures_box:
        item.box = value
    else:
        if n_structures_box == 1:
            item.box = np.broadcast_to(value[0]._value, (n_structures_trajectory,3,3)) * value.unit
        else:
            raise ValueError("box and coordinates have different shape")

    pass

