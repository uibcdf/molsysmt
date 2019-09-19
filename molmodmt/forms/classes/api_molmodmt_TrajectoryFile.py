from os.path import basename as _basename
from molmodmt.utils.exceptions import *
from molmodmt.native.trajectory_file import TrajectoryFile as _molmodmt_TrajectoryFile

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _molmodmt_TrajectoryFile : form_name,
    'molmodmt.TrajectoryFile': form_name
}

def duplicate(item):

    from copy import deepcopy

    tmp_item = _molmodmt_TrajectoryFile(filename=item.name, mode='read')
    tmp_item.atom_indices = deepcopy(item.atom_indices)

    # close de file if it was closed
    # put the needle in the same position of original file of item

    return tmp_item

