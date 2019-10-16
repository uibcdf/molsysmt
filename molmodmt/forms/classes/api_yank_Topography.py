from os.path import basename as _basename
from yank import Topography as _yank_Topography

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    'yank.Topography': form_name,
    _yank_Topography: form_name
}

def to_openmm_Topology(item):

    return item.topology()

###### Get

## system

def get_form_from_system(item, indices=None, frame_indices=None):

    from molmodmt import _get_form
    return _get_form(item)

