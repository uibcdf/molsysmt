from molmodmt.utils.exceptions import *
from os.path import basename as _basename
from pytraj import Trajectory as _pytraj_Trajectory

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    'pytraj.Trajectory' : form_name,
    _pytraj_Trajectory : form_name
    }

## Methods

def to_nglview(item):

    from nglview import show_pytraj as _show_pytraj
    tmp_view = _show_pytraj(item)
    return tmp_view


###### Get

## system

def get_form_from_system(item, indices=None, frame_indices=None):

    from molmodmt import get_form
    return get_form(item)

