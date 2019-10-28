from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].replace('api_','')+':seq'

is_form={
    'secondary_structure_abc:seq' : form_name
}


def get_shape(item):
    raise NotImplementedError

def select_with_MDTraj(item, selection):
    raise NotImplementedError

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

