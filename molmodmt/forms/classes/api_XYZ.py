from os.path import basename as _basename
from simtk.unit.quantity import Quantity

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
}

def this_Quantity_is_XYZ(item):

    from numpy import ndarray

    is_XYZ = False

    list_base_dimensions = list(item.unit.iter_base_dimensions())

    if len(list_base_dimensions)==1:
        if list_base_dimensions[0][0].name == 'length':
            is_XYZ = True

    return is_XYZ

def extract_subsystem(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def duplicate(item):

    raise NotImplementedError

###### Get

## atom

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    tmp_coordinates=None

    if len(item.shape)==3:
        tmp_coordinates = item[:,indices,:]
    elif len(item.shape)==2:
        from numpy import zeros
        n_frames=1
        n_atoms=item.shape[0]
        tmp_coordinates = zeros([n_frames, n_atoms, 3])*item.unit
        tmp_coordinates[0,:,:] = item[:,:]
        tmp_coordinates = tmp_coordinates[:,indices,:]

    tmp_coordinates = tmp_coordinates[frame_indices,:,:]

    return tmp_coordinates

## system

def get_coordinates_from_system(item, indices='all', frame_indices='all'):

    tmp_coordinates=None

    if len(item.shape)==3:
        tmp_coordinates = item
    elif len(item.shape)==2:
        from numpy import zeros
        n_frames=1
        n_atoms=item.shape[0]
        tmp_coordinates = zeros([n_frames, n_atoms, 3])*item.unit
        tmp_coordinates[0,:,:] = item[:,:]

    tmp_coordinates = tmp_coordinates[frame_indices,:,:]

    return tmp_coordinates

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    n_frames=0
    if len(item.shape)==3:
        n_frames = item.shape[0]
    elif len(item.shape)==2:
        n_frames = 1

    return n_frames

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    n_atoms=0
    if len(item.shape)==3:
        n_atoms = item.shape[1]
    elif len(item.shape)==2:
        n_atoms = item.shape[0]

    return n_atoms

def get_box_from_system(item, indices='all', frame_indices='all'):

    return None

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    return None

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

