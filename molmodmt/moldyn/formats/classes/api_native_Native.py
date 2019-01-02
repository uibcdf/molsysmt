from os.path import basename as _basename
from moldynmt.native import Native as _native_Native

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    'native.Native' : form_name,
    'moldynmt.native.Native' : form_name,
    _native_Native  : form_name
    }

def get_shape(item):

    return item.trajectory.n_frames, item.trajectory.n_atoms

def to_mdtraj_Trajectory(item):

    return item.trajectory

def to_nglview(item):
    from nglview import show_mdtraj as _nglview_show_mdtraj
    return _nglview_show_mdtraj(item.trajectory)
