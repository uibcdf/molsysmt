from molsysmt._private.digestion import digest

###### Set

@digest(form='molsysmt.Structures')
def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None):

    if is_all(indices):
        if is_all(structure_indices):
            item.structures.coordinates = value              
            item.structures.n_structures = value.shape[0]
            item.structures.n_atoms = value.shape[1]
        else:
            item.structures.coordinates[structure_indices,:,:] = value[:,:,:]
    else:
        if is_all(structure_indices):
            item.structures.coordinates[:,indices,:] = value[:,:,:]
        else:
            item.structures.coordinates[np.ix_(structure_indices, indices)]=value[:,:,:]

    pass

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

