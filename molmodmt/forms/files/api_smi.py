from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]


is_form = {
    'smi': form_name,
    'SMI': form_name
    }

def extract_subsystem(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def duplicate(item):

    raise NotImplementedError

###### Get

## system

def get_form_from_system(item, indices='all', frame_indices='all'):

    from molmodmt import get_form
    return get_form(item)

