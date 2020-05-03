from os.path import basename as _basename
from os import remove as _remove

form_name=_basename(__file__).split('.')[0][4:]+':id'

is_form = {
    'chembl:id': form_name,
    'ChEMBL:id': form_name
    }

info=["",""]

def to_UniProt_id(form_id):
    pass

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

