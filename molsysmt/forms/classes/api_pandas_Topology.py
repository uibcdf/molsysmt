from os.path import basename as _basename
from pandas import DataFrame

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    'pandas.DataFrame' : form_name,
    DataFrame : form_name
}

info=["",""]

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

def select_with_MolSysMT(item, selection):

    from molsysmt.native.selector import dataframe_select
    atom_indices = dataframe_select(item, selection)
    return atom_indices

###### Get

## atom


## system

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

