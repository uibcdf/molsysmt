from molsysmt._private.exceptions import *

from molsysmt.item.mdtraj_XTCTrajectoryFile.is_mdtraj_XTCTrajectoryFile import is_mdtraj_XTCTrajectoryFile as is_form
from molsysmt.item.mdtraj_XTCTrajectoryFile.extract import extract
from molsysmt.item.mdtraj_XTCTrajectoryFile.add import add
from molsysmt.item.mdtraj_XTCTrajectoryFile.append_structures import append_structures
from molsysmt.item.mdtraj_XTCTrajectoryFile.get import *
from molsysmt.item.mdtraj_XTCTrajectoryFile.set import *

form_name='mdtraj.XTCTrajectoryFile'
form_type='class'
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

    from molsysmt.item.mdtraj_XTCTrajectoryFile import to_molsysmt_Structures as mdtraj_XTCTrajectoryFile_to_molsysmt_Structures

    tmp_item = mdtraj_XTCTrajectoryFile_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

