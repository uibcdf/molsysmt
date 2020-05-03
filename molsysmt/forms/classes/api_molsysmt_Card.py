from os.path import basename as _basename
from molsysmt.utils.exceptions import *
from molsysmt.native.card import Card as _molsysmt_Card

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _molsysmt_Card : form_name,
    'molsysmt.Card': form_name
}

info=["",""]

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

