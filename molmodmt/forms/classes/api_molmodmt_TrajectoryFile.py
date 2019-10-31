from os.path import basename as _basename
from molmodmt.utils.exceptions import *
from molmodmt.native.trajectory_file import TrajectoryFile as _molmodmt_TrajectoryFile

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _molmodmt_TrajectoryFile : form_name,
    'molmodmt.TrajectoryFile': form_name
}

def extract_subsystem(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def duplicate(item):

    return item.duplicate()

###### Get

## system

def get_form_from_system(item, indices='all', frame_indices='all'):

    from molmodmt import get_form
    return get_form(item)

