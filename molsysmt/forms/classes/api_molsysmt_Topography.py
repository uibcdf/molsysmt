from os.path import basename as _basename
from molsysmt.utils.exceptions import *
from molsysmt.native.topography import Topography as _molsysmt_Topography

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _molsysmt_Topography : form_name,
    'molsysmt.Topography': form_name
}

info=["",""]
with_topology=False
with_trajectory=False

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        return item.extract(atom_indices=atom_indices, frame_indices=frame_indices)

def copy(item):

    return item.copy()

###### Get

## system

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

