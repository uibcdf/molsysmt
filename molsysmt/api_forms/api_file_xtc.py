from molsysmt._private.exceptions import *

from molsysmt.form.file_xtc.is_file_xtc import is_file_xtc as is_form
from molsysmt.form.file_xtc.extract import extract
from molsysmt.form.file_xtc.add import add
from molsysmt.form.file_xtc.append_structures import append_structures
from molsysmt.form.file_xtc.get import *
from molsysmt.form.file_xtc.set import *

form_name='file:xtc'
form_type='file'
form_info=["",""]

form_attributes = {

    'atom_index' : False,
    'atom_id' : False,
    'atom_name' : False,
    'atom_type' : False,

    'bond_index' : False,
    'bond_id' : False,
    'bond_name' : False,
    'bond_type' : False,
    'bond_order' : False,

    'group_index' : False,
    'group_id' : False,
    'group_name' : False,
    'group_type' : False,

    'component_index' : False,
    'component_id' : False,
    'component_name' : False,
    'component_type' : False,

    'molecule_index' : False,
    'molecule_id' : False,
    'molecule_name' : False,
    'molecule_type' : False,

    'chain_index' : False,
    'chain_id' : False,
    'chain_name' : False,
    'chain_type' : False,

    'entity_index' : False,
    'entity_id' : False,
    'entity_name' : False,
    'entity_type' : False,

    'coordinates' : True,
    'velocities' : False,
    'box' : True,
    'time' : True,
    'step' : True,

    'forcefield_parameters' : False,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}

def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_xtc import to_molsysmt_Structures as file_xtc_to_molsysmt_Structures

    tmp_item = file_xtc_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_mdtraj_XTCTrajectoryFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_xtc import to_mdtraj_XTCTrajectoryFile as file_xtc_to_mdtraj_XTCTrajectoryFile

    tmp_item = file_xtc_to_mdtraj_XTCTrajectoryFile(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_xtc import to_mdtraj_Trajectory as file_xtc_to_mdtraj_Trajectory

    tmp_item = file_xtc_to_mdtraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

