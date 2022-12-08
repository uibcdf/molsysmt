from molsysmt.form.openmm_Context.is_openmm_Context import is_openmm_Context as is_form
from molsysmt.form.openmm_Context.extract import extract
from molsysmt.form.openmm_Context.add import add
from molsysmt.form.openmm_Context.append_structures import append_structures
from molsysmt.form.openmm_Context.get import *
from molsysmt.form.openmm_Context.set import *
from molsysmt.form.openmm_Context.iterators import StructuresIterator, TopologyIterator
from .form_attributes import form_attributes

form_name = 'openmm.Context'
form_type = 'class'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['atom_index'] = True
form_attributes['coordinates'] = True
form_attributes['velocities'] = True
form_attributes['box'] = True
form_attributes['time'] = True
form_attributes['step'] = True
form_attributes['forcefield'] = True
form_attributes['temperature'] = True


def to_openmm_System(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Context import to_openmm_System as openmm_Context_to_openmm_System

    return openmm_Context_to_openmm_System(item, atom_indices=atom_indices)

def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Context import to_molsysmt_Structures as openmm_Context_to_molsysmt_Structures

    return openmm_Context_to_molsysmt_Structures(item, atom_indices=atom_indices)

