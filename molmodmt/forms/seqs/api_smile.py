from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].replace('api_','')+':seq'

is_form={
    'smile:seq' : form_name,
    'SMILE:seq' : form_name
}

def get_shape(item):
    raise NotImplementedError

def select_with_mdtraj(item, selection):
    raise NotImplementedError

def extract_subsystem(item, atom_indices=None, frame_indices=None):
    raise NotImplementedError

###### Get

## system

def get_form_from_system(item, indices=None, frame_indices=None):

    from molmodmt import _get_form
    return _get_form(item)

