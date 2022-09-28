from molsysmt._private.digestion import digest

###### Set

## System

@digest(form='molsysmt.Structures')
def set_box_to_system(item, indices='all', structure_indices='all', value=None):

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

