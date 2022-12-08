from molsysmt.form.openmm_System.is_openmm_System import is_openmm_System as is_form
from molsysmt.form.openmm_System.extract import extract
from molsysmt.form.openmm_System.add import add
from molsysmt.form.openmm_System.append_structures import append_structures
from molsysmt.form.openmm_System.get import *
from molsysmt.form.openmm_System.set import *
from molsysmt.form.openmm_System.iterators import StructuresIterator, TopologyIterator
from .form_attributes import form_attributes

form_name = 'openmm.System'
form_type = 'class'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['atom_index'] = True
form_attributes['atom_id'] = True
form_attributes['atom_name'] = True
form_attributes['atom_type'] = True
form_attributes['bond_index'] = True
form_attributes['bond_id'] = True
form_attributes['bond_name'] = True
form_attributes['bond_type'] = True
form_attributes['bond_order'] = True
form_attributes['group_index'] = True
form_attributes['group_id'] = True
form_attributes['group_name'] = True
form_attributes['group_type'] = True
form_attributes['component_index'] = True
form_attributes['molecule_index'] = True
form_attributes['molecule_id'] = True
form_attributes['molecule_name'] = True
form_attributes['molecule_type'] = True
form_attributes['chain_index'] = True
form_attributes['chain_id'] = True
form_attributes['chain_name'] = True
form_attributes['chain_type'] = True
form_attributes['entity_index'] = True
form_attributes['entity_id'] = True
form_attributes['entity_name'] = True
form_attributes['entity_type'] = True
form_attributes['box'] = True
form_attributes['forcefield'] = True
form_attributes['temperature'] = True
form_attributes['pressure'] = True
form_attributes['integrator'] = True
form_attributes['damping'] = True


def to_openmm_Context(item, molecular_system=None, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_System import to_openmm_Context as openmm_System_to_openmm_Context

    return openmm_System_to_openmm_Context(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_openmm_Simulation(item, molecular_system=None, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_System import to_openmm_Simulation as openmm_System_to_openmm_Simulation

    return openmm_System_to_openmm_Simulation(item, atom_indices=atom_indices, structure_indices=structure_indices)
