from os.path import basename as _basename
from moldynmt.native import Native as _moldynmt_Native

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    'moldynmt.native.Native' : form_name,
    _moldynmt_Native : form_name
}

def to_nglview(item):

    from nglview import show_mdtraj as _nglview_show_mdtraj

def to_mdtraj_Trajectory(item):
    return item.trajectory

def select_with_mdtraj(item, selection):
    return item.trajectory.topology.select(selection)

