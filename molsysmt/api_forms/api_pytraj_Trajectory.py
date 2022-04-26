from molsysmt._private.exceptions import *
import numpy as np

from molsysmt.form.pytraj_Trajectory.is_pytraj_Trajectory import is_pytraj_Trajectory as is_form
from molsysmt.form.pytraj_Trajectory.extract import extract
from molsysmt.form.pytraj_Trajectory.add import add
from molsysmt.form.pytraj_Trajectory.append_structures import append_structures
from molsysmt.form.pytraj_Trajectory.get import *
from molsysmt.form.pytraj_Trajectory.set import *

form_name='pytraj.Trajectory'
form_type='class'
form_info=["",""]

form_attributes = {

    'atom_index' : True,
    'atom_id' : True,
    'atom_name' : True,
    'atom_type' : True,

    'bond_index' : True,
    'bond_id' : True,
    'bond_name' : True,
    'bond_type' : True,
    'bond_order' : True,

    'group_index' : True,
    'group_id' : True,
    'group_name' : True,
    'group_type' : True,

    'component_index' : True,
    'component_id' : False,
    'component_name' : False,
    'component_type' : False,

    'molecule_index' : True,
    'molecule_id' : True,
    'molecule_name' : True,
    'molecule_type' : True,

    'chain_index' : True,
    'chain_id' : True,
    'chain_name' : True,
    'chain_type' : True,

    'entity_index' : False,
    'entity_id' : False,
    'entity_name' : False,
    'entity_type' : False,

    'coordinates' : True,
    'velocities' : False,
    'box' : True,
    'time' : False,
    'step' : False,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}

def to_pytraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.pytraj_Trajectory import to_pytraj_Topology as pytraj_Trajectory_to_pytraj_Topology

    tmp_item = pytraj_Trajectory_to_pytraj_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.pytraj_Trajectory import to_molsysmt_MolSys as pytraj_Trajectory_to_molsysmt_MolSys

    tmp_item = pytraj_Trajectory_to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.pytraj_Trajectory import to_molsysmt_Topology as pytraj_Trajectory_to_molsysmt_Topology

    tmp_item = pytraj_Trajectory_to_molsysmt_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.pytraj_Trajectory import to_molsysmt_Structures as pytraj_Trajectory_to_molsysmt_Structures

    tmp_item = pytraj_Trajectory_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                        structure_indices=structure_indices, check=False)

    return tmp_item

