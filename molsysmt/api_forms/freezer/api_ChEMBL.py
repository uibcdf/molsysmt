from os.path import basename as _basename
from os import remove as _remove

form_name=_basename(__file__).split('.')[0][4:]+':id'

is_form = {
    'chembl:id': form_name,
    'ChEMBL:id': form_name
    }

info=["",""]
with_topology=True
with_trajectory=False

def to_UniProt_id(form_id):
    pass

def extract(item, atom_indices='all', structure_indices='all'):

    if (atom_indices is 'all') and (structure_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

###### Get

## system

def get_form_from_system(item, indices='all', structure_indices='all'):

    return form_name

