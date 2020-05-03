from os.path import basename as _basename
from yank import Topography as _yank_Topography

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    'yank.Topography': form_name,
    _yank_Topography: form_name
}

info=["",""]

def to_openmm_Topology(item, atom_indices='all', frame_indices='all'):

    from .api_openmm_Topology import extract as extract_openmm_Topology
    tmp_item = item.topology()
    tmp_item = extract_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

###### Get

## system

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

