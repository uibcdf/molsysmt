from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].replace('api_','')+':seq'

is_form={
    'secondary_structure_dssp:seq' : form_name
}

info=["",""]

_dssp_to_abc = {"I" : "c", # coil
                "S" : "c",
                "H" : "a", # helix
                "E" : "b", # sheet
                "G" : "c",
                "B" : "b",
                "T" : "c",
                "C" : "c",
                "X" : "X"} # undefined

def to_secondary_structure_abc(item, atom_indices='all', frame_indices='all'):
    raise NotImplementedError

def select_with_MDTraj(item, selection):
    raise NotImplementedError

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

