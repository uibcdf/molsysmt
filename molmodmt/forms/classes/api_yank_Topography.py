from os.path import basename as _basename
from yank import Topography as _yank_Topography

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    'yank.Topography': form_name,
    _yank_Topography: form_name
}

def to_openmm_Topology(item, atom_indices=None, frame_indices=None):

    from .api_openmm_Topology import extract_subsystem as extract_openmm_Topology
    tmp_item = item.topology()
    tmp_item = extract_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def extract_subsystem(item, atom_indices=None, frame_indices=None):

    if (atom_indices is None) and (frame_indices is None):
        return item
    else:
        raise NotImplementedError

def duplicate(item):

    raise NotImplementedError

###### Get

## system

def get_form_from_system(item, indices=None, frame_indices=None):

    from molmodmt import get_form
    return get_form(item)

