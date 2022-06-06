from molsysmt._private.exceptions import *

from molsysmt.item.openmm_System.is_openmm_System import is_openmm_System as is_form
from molsysmt.item.openmm_System.extract import extract
from molsysmt.item.openmm_System.add import add
from molsysmt.item.openmm_System.append_structures import append_structures
from molsysmt.item.openmm_System.get import *
from molsysmt.item.openmm_System.set import *

form_name='openmm.System'
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

    'entity_index' : True,
    'entity_id' : True,
    'entity_name' : True,
    'entity_type' : True,

    'coordinates' : False,
    'velocities' : False,
    'box' : True,
    'time' : False,
    'step' : False,

    'forcefield' : True,
    'temperature' : True,
    'pressure' : True,
    'integrator' : True,
    'damping' : True,
}

def to_openmm_Context(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.item.openmm_System import to_openmm_Context as openmm_System_to_openmm_Context

    tmp_item = openmm_System_to_openmm_Context(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_openmm_Simulation(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.item.openmm_System import to_openmm_Simulation as openmm_System_to_openmm_Simulation

    tmp_item = openmm_System_to_openmm_Simulation(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

