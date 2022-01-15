from molsysmt._private_tools.exceptions import *

from molsysmt.tools.molsysmt_Trajectory.extract import extract
from molsysmt.tools.molsysmt_Trajectory.add import add
from molsysmt.tools.molsysmt_Trajectory.merge import merge
from molsysmt.tools.molsysmt_Trajectory.append_frames import append_frames
from molsysmt.tools.molsysmt_Trajectory.concatenate_frames import concatenate_frames
from molsysmt.tools.molsysmt_Trajectory.get import *
from molsysmt.tools.molsysmt_Trajectory.set import *

form_name='molsysmt.Trajectory'
form_type='class'
form_info=["",""]

form_elements = {
    'atoms' : False,
    'bonds' : False,
    'groups' : False,
    'component' : False,
    'molecule' : False,
    'chain' : False,
    'entity' : False,
        }

form_attributes = {

    'atom_id' : False,
    'atom_name' : False,
    'atom_type' : False,

    'bond_id' : False,
    'bond_name' : False,
    'bond_type' : False,

    'group_id' : False,
    'group_name' : False,
    'group_type' : False,

    'component_id' : False,
    'component_name' : False,
    'component_type' : False,

    'molecule_id' : False,
    'molecule_name' : False,
    'molecule_type' : False,

    'chain_id' : False,
    'chain_name' : False,
    'chain_type' : False,

    'entity_id' : False,
    'entity_name' : False,
    'entity_type' : False,

    'coordinates' : True,
    'velocities' : False,
    'box' : True,
    'time' : True,
    'step' : True,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}


# Methods

def to_molsysmt_TrajectoryDict(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.tools.molsysmt_Trajectory import to_molsysmt_TrajectoryDict as molsysmt_Trajectory_to_molsysmt_TrajectoryDict

    tmp_item = molsysmt_Trajectory_to_molsysmt_TrajectoryDict(item, atom_indices=atom_indices, frame_indices=frame_indices, check_form=False)

    return tmp_item

def to_XYZ(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.tools.molsysmt_Trajectory import to_XYZ as molsysmt_Trajectory_to_XYZ

    tmp_item = molsysmt_Trajectory_to_XYZ(item, atom_indices=atom_indices, frame_indices=frame_indices, check_form=False)

    return tmp_item


