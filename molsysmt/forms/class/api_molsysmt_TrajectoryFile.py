from os.path import basename as _basename
from molsysmt._private_tools.exceptions import *
from molsysmt.native.trajectory_file import TrajectoryFile as _molsysmt_TrajectoryFile

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _molsysmt_TrajectoryFile : form_name,
    'molsysmt.TrajectoryFile': form_name
}

info=["",""]
with_topology=False
with_coordinates=True
with_box=True
with_parameters=False

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    return item.copy()

###### Get

## system

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

