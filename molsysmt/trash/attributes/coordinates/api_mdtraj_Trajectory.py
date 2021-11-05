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
    return coordinates

def to_openmm(coordinates):

    # mdtraj uses nanometers: see http://mdtraj.org/development/api/generated/mdtraj.Trajectory.html
    # openmm uses nanometers

    from openmm.unit import nanometers as _nanometers
    tmp_coordinates = coordinates*_nanometers
    return tmp_coordinates

