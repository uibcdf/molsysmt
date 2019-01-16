from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _xxxx_Xxxx : form_name
}

def get_shape(item):
    raise NotImplementedError

def select_with_mdtraj(item, selection):
    raise NotImplementedError

def extract_atoms_list(item, atoms_list):
    raise NotImplementedError
