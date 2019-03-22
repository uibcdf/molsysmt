from os.path import basename as _basename
from molmodmt.utils.exceptions import *

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'xtc': form_name,
    'XTC': form_name
    }

def to_mdtraj_Trajectory(item, topology=None):

    if topology is None:
        raise BadCallError(BadCallMessage)

    from mdtraj import load as _mdtraj_load
    tmp_form = _mdtraj_load(item, top=topology)
    del(_mdtraj_load)
    return tmp_form

def to_molmod(item, topology=None, frames=None):

    from molmodmt.native.io_molmod import from_xtc as _from_xtc
    return _from_xtc(item, topology=topology, frames=frames)

