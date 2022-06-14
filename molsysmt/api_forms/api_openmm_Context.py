from molsysmt._private.exceptions import *

from molsysmt.item.openmm_Context.is_openmm_Context import is_openmm_Context as is_form
from molsysmt.item.openmm_Context.extract import extract
from molsysmt.item.openmm_Context.add import add
from molsysmt.item.openmm_Context.append_structures import append_structures
from molsysmt.item.openmm_Context.get import *
from molsysmt.item.openmm_Context.set import *

form_name='openmm.Context'
form_type='class'
form_info=["",""]

form_attributes = {

    'atom_index' : True,
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
    'velocities' : True,
    'box' : True,
    'time' : True,
    'step' : True,

    'forcefield' : True,
    'temperature' : True,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}

def to_openmm_System(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.openmm_Context import to_openmm_System as openmm_Context_to_openmm_System

    tmp_item = openmm_Context_to_openmm_System(item, atom_indices=atom_indices, check=False)

    return tmp_item


