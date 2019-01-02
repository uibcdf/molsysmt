from os.path import basename as _basename
from molsysmt.native import Native as _native_Native

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    'native': form_name,
    'Native': form_name,
    'native.Native': form_name,
    'molsysmt.native.Native': form_name,
    _native_Native : form_name
}

def to_nglview(item):

    from .api_mdtraj_Trajectory import to_nglview as _mdtraj_Trajectory_to_nglview
    tmp_view = _mdtraj_Trajectory_to_nglview(item.trajectory)
    del(_mdtraj_Trajectory_to_nglview)
    return tmp_view

def to_openmm_Topology(item):

    return item.topology.to_openmm()

def to_mdtraj_Topology(item):

    return item.topology

def to_mdtraj_Trajectory(item):

    from mdtraj.core.trajectory import Trajectory as _mdtraj_trajectory
    tmp_form = _mdtraj_trajectory(item.positions._value, item.topology)
    del(_mdtraj_trajectory)
    return tmp_form

def to_mdtraj(item):

    return to_mdtraj_Trajectory(item)

def to_pdb(item,filename):

    item.trajectory.save_pdb(filename)
    pass

def select_with_mdtraj(item, selection):
    return item.select(selection)

