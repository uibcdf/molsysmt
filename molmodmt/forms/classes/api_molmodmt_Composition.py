from os.path import basename as _basename
from molmodmt.utils.exceptions import *
from molmodmt.native.composition import Composition as _molmodmt_Composition

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _molmodmt_Composition : form_name,
    'molmodmt.Composition': form_name
}

def extract_subsystem(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        return item.extract(atom_indices=atom_indices, frame_indices=frame_indices)

def duplicate(item):

    return item.duplicate()

###### Get

## system

def get_form_from_system(item, indices='all', frame_indices='all'):

    from molmodmt import get_form
    return get_form(item)

