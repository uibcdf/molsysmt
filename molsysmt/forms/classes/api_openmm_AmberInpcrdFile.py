from os.path import basename as _basename
from simtk.openmm.app import AmberInpcrdFile as _openmm_AmberInpcrdFile

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _openmm_AmberInpcrdFile : form_name,
    'openmm.AmberInpcrdFile' : form_name
}

info=["",""]
with_topology=False
with_coordinates=True
with_box=True
with_bonds=False
with_parameters=False

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

def merge(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def concatenate(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def add(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def append(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

##### Set

## Atom

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## System

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

