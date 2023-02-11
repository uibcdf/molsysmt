from molsysmt.form.openmm_CharmmPsfFile.is_openmm_CharmmPsfFile import is_openmm_CharmmPsfFile as is_form
from molsysmt.form.openmm_CharmmPsfFile.extract import extract
from molsysmt.form.openmm_CharmmPsfFile.add import add
from molsysmt.form.openmm_CharmmPsfFile.append_structures import append_structures
from molsysmt.form.openmm_CharmmPsfFile.get import *
from molsysmt.form.openmm_CharmmPsfFile.set import *
from molsysmt.form.openmm_CharmmPsfFile.iterators import StructuresIterator, TopologyIterator
from .form_attributes import form_attributes

form_name = 'openmm.CharmmPsfFile'
form_type = 'class'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['atom_index'] = True
form_attributes['atom_id'] = True
form_attributes['atom_name'] = True
form_attributes['atom_type'] = True
form_attributes['group_index'] = True
form_attributes['group_id'] = True
form_attributes['group_name'] = True
form_attributes['group_type'] = True
form_attributes['coordinates'] = True
form_attributes['box'] = True

def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_CharmmPsfFile import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology

    return openmm_Topology_to_molsysmt_Topology(item, atom_indices=atom_indices)

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Topology import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology

    return openmm_Topology_to_molsysmt_Topology(item, atom_indices=atom_indices)

