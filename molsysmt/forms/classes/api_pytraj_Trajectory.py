from molsysmt.utils.exceptions import *
from os.path import basename as _basename
from pytraj import Trajectory as _pytraj_Trajectory

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    'pytraj.Trajectory' : form_name,
    _pytraj_Trajectory : form_name
    }

info=["",""]
with_topology=True
with_trajectory=True

## Methods

def to_nglview(item):

    from nglview import show_pytraj as _show_pytraj
    tmp_view = _show_pytraj(item)
    return tmp_view

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

