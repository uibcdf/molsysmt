from molsysmt._private.exceptions import *

from molsysmt.item.openmm_GromacsTopFile.is_openmm_GromacsTopFile import is_openmm_GromacsTopFile as is_form
from molsysmt.item.openmm_GromacsTopFile.extract import extract
from molsysmt.item.openmm_GromacsTopFile.add import add
from molsysmt.item.openmm_GromacsTopFile.append_structures import append_structures
from molsysmt.item.openmm_GromacsTopFile.get import *
from molsysmt.item.openmm_GromacsTopFile.set import *

form_name='openmm.GromacsTopFile'
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

    'component_index' : False,
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

    'coordinates' : False,
    'velocities' : False,
    'box' : False,
    'time' : False,
    'step' : False,

    'forcefield_parameters' : False,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}

def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.openmm_GromacsTopFile import to_openmm_Topology as openmm_GromacsTopFile_to_openmm_Topology

    tmp_item = openmm_GromacsTopFile_to_openmm_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.openmm_GromacsTopFile import to_molsysmt_Topology as openmm_GromacsTopFile_to_molsysmt_Topology

    tmp_item = openmm_GromacsTopFile_to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

