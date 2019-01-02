from os.path import basename as _basename
from mdtraj.core.trajectory import Trajectory as _mdtraj_Trajectory

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdtraj_Trajectory:form_name
    }

def to_nglview(item):
    from nglview import show_mdtraj as _nglview_show_mdtraj
    return _nglview_show_mdtraj(item)

def to_native_Native(item):

    from moldynmt.native import Native as _Native

    return _Native(item)

def to_pdb(item,output_file):

    return item.save(output_file)

def get_shape(item):

    return item.n_frames, item.n_atoms
