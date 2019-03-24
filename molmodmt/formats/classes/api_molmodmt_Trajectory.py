from os.path import basename as _basename
from molmodmt.utils.exceptions import *
from molmodmt.native.trajectory import Trajectory as _molmodmt_Trajectory

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _molmodmt_Trajectory : form_name
}

def get_shape(item):
    raise NotImplementedError(NotImplementedMessage)

def select_with_mdtraj(item, selection):
    raise NotImplementedError(NotImplementedMessage)

def extract_atoms_list(item, atoms_list):
    raise NotImplementedError(NotImplementedMessage)

def to_mdtraj_Trajectory(item):
    from molmodmt.native.io_trajectory import to_mdtraj_Trajectory as _to_mdtraj_Trajectory
    return _to_mdtraj_Trajectory(item)

def to_nglview(item):

    from .api_mdtraj_Trajectory import to_nglview as _mdtraj_to_nglview

    if type(item) in [list,tuple]:
        tmp_item = []
        for ii in item:
            tmp_item.append(to_mdtraj_Trajectory(ii))
    else:
        tmp_item = to_mdtraj_Trajectory(item)

    return _mdtraj_to_nglview(tmp_item)

