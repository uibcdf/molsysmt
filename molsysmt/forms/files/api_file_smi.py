from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
from molsysmt.molecular_system import molecular_system_components

form_name='file:smi'


is_form = {
        'file:smi': form_name,
        'file:SMI': form_name
    }

info=["",""]

has = molecular_system_components.copy()
for ii in ['elements']:
    has[ii]=True

def to_file_smi(item, molecular_system, atom_indices='all', frame_indices='all', output_filename=None, copy_if_all=False):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        if copy_if_all:
            tmp_item = extract_item(item)
            tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
        else:
            tmp_item = item
            tmp_molecular_system = molecular_system
    else:
        tmp_item = extract_item(item, atom_indices=atom_indices, frame_indices=frame_indices)
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def extract_item(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return NotImplementedError()
    else:
        raise NotImplementedError()

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError()

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError()


###### Get

## system

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

