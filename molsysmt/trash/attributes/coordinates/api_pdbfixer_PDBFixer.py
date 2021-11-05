from os.path import basename as _basename
from mdtraj.core.trajectory import Trajectory as _mdtraj_Trajectory

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdtraj_Trajectory:form_name,
    'mdtraj.Trajectory':form_name
    }

def to_mdtraj(coordinates):

    return to_mdtraj_Trajectory(coordinates)

def to_mdtraj_Trajectory(coordinates):
    raise NotImplementedError

def to_openmm(coordinates):

    return coordinates

