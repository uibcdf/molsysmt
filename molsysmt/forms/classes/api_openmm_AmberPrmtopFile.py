from os.path import basename as _basename
from simtk.openmm.app import AmberPrmtopFile as _openmm_AmberPrmtopFile

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _openmm_AmberPrmtopFile : form_name,
    'openmm.AmberPrmtopFile' : form_name
}

info=["",""]

def to_mdtraj_Trajectory(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_mdtraj_Topology(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_nglview(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

##### Set

## Atom

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## System

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

