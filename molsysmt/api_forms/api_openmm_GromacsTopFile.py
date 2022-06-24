from molsysmt._private.exceptions import *
from molsysmt.item.openmm_GromacsTopFile.is_openmm_GromacsTopFile import is_openmm_GromacsTopFile as is_form
from molsysmt.item.openmm_GromacsTopFile.extract import extract
from molsysmt.item.openmm_GromacsTopFile.add import add
from molsysmt.item.openmm_GromacsTopFile.append_structures import append_structures
from molsysmt.item.openmm_GromacsTopFile.get import *
from molsysmt.item.openmm_GromacsTopFile.set import *
from .form_attributes import form_attributes

form_name = 'openmm.GromacsTopFile'
form_type = 'class'
form_info = ["",""]

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
form_attributes['molecule_index'] = True
form_attributes['molecule_id'] = True
form_attributes['molecule_name'] = True
form_attributes['molecule_type'] = True
form_attributes['chain_index'] = True
form_attributes['chain_id'] = True
form_attributes['chain_name'] = True
form_attributes['chain_type'] = True


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

	from molsysmt.item.openmm_GromacsTopFile import to_openmm_Topology as openmm_GromacsTopFile_to_openmm_Topology

	return openmm_GromacsTopFile_to_openmm_Topology(item, atom_indices=atom_indices, check=False)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

	from molsysmt.item.openmm_GromacsTopFile import to_molsysmt_Topology as openmm_GromacsTopFile_to_molsysmt_Topology

	return openmm_GromacsTopFile_to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)


