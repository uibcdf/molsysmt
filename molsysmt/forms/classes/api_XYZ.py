from os.path import basename as _basename
from simtk.unit.quantity import Quantity

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
}

info=["",""]
with_topology=False
with_trajectory=True

def item_in_good_shape(item):

    tmp_item = item

    if len(tmp_item.shape)==2:
        from numpy import expand_dims
        tmp_item = expand_dims(tmp_item, axis=0)*item.unit

    return tmp_item

def this_Quantity_has_XYZ_shape(item):

    # Only np.arrays of shape [n_frames, n_particles, coordinates] or [n_particles, coordinates] are
    # admitted

    has_right_shape = False

    shape = item.shape

    if len(shape)==3 and shape[-1]==3:
        has_right_shape = True
    elif len(shape)==2 and shape[-1]==3:
        has_right_shape = True

    return has_right_shape

def this_Quantity_is_XYZ(item):

    # Only np.arrays of shape [n_frames, n_particles, coordinates] or [n_particles, coordinates] are
    # admitted

    from numpy import ndarray

    is_length = False

    list_base_dimensions = list(item.unit.iter_base_dimensions())

    if len(list_base_dimensions)==1:
        if list_base_dimensions[0][0].name == 'length':
            is_length = True

    has_right_shape = this_Quantity_has_XYZ_shape(item)

    return (has_right_shape and is_length)

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

###### Get

## atom

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    tmp_item = item_in_good_shape(item)
    tmp_coordinates=tmp_item[:,:,:]

    if indices is not 'all':
        tmp_coordinates = tmp_item[:,indices,:]

    if frame_indices is not 'all':
        tmp_coordinates = tmp_coordinates[frame_indices,:,:]

    return tmp_coordinates

def get_n_atoms_from_atom(item, indices='all', frame_indices='all'):

    if indices=='all':
        tmp_item = item_in_good_shape(item)
        return tmp_item.shape[1]
    else:
        return len(indices)

def get_n_frames_from_atom(item, indices='all', frame_indices='all'):

    tmp_item = item_in_good_shape(item)
    return tmp_item.shape[0]

def get_form_from_atom(item, indices='all', frame_indices='all'):

    return form_name

## system

def get_coordinates_from_system(item, indices='all', frame_indices='all'):

    tmp_item = item_in_good_shape(item)
    tmp_coordinates=tmp_item[:,:,:]
    if frame_indices is not 'all':
        tmp_coordinates = tmp_coordinates[frame_indices,:,:]

    return tmp_coordinates

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    tmp_item = item_in_good_shape(item)
    return tmp_item.shape[1]

def get_box_from_system(item, indices='all', frame_indices='all'):

    return None

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    return None

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    tmp_item = item_in_good_shape(item)
    return tmp_item.shape[0]


def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

