from os.path import basename as _basename
from molmodmt.moldyn_native import Native as _Native

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    'moldyn.Native' : form_name,
    _Native : form_name
}

def to_nglview(item):

    from nglview import show_mdtraj as _nglview_show_mdtraj

def to_mdtraj_Trajectory(item):
    return item.trajectory

def select_with_mdtraj(item, selection):
    return item.trajectory.topology.select(selection)

def get_shape(item):

    return item.trajectory.n_frames, item.trajectory.n_atoms

