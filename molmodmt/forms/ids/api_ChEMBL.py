from os.path import basename as _basename
from os import remove as _remove

form_name=_basename(__file__).split('.')[0][4:]+':id'

is_form = {
    'chembl:id': form_name,
    'ChEMBL:id': form_name
    }

def to_UniProt_id(form_id):
    pass

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

