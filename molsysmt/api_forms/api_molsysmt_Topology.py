from molsysmt._private.exceptions import *
from molsysmt.item.molsysmt_Topology.is_molsysmt_Topology import is_molsysmt_Topology as is_form
from molsysmt.item.molsysmt_Topology.extract import extract
from molsysmt.item.molsysmt_Topology.add import add
from molsysmt.item.molsysmt_Topology.append_structures import append_structures
from molsysmt.item.molsysmt_Topology.get import *
from molsysmt.item.molsysmt_Topology.set import *
from .form_attributes import form_attributes

form_name = 'molsysmt.Topology'
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
form_attributes['bonded_atoms'] = True
form_attributes['group_index'] = True
form_attributes['group_id'] = True
form_attributes['group_name'] = True
form_attributes['group_type'] = True
form_attributes['component_index'] = True
form_attributes['component_id'] = True
form_attributes['component_name'] = True
form_attributes['component_type'] = True
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


def to_string_aminoacids3(item, molecular_system, atom_indices='all', structure_indices='all'):

	from molsysmt.item.molsysmt_Topology import to_string_aminoacids3 as molsysmt_Topology_to_string_aminoacids3


	from molsysmt.item.molsysmt_Topology import get_group_index_from_atom as get_group_index_from_atom_molsysmt_Topology

	group_indices = get_group_index_from_atom_molsysmt_Topology(item, indices=atom_indices, check=False)
	group_indices = np.unique(group_indices)
	return molsysmt_Topology_to_string_aminoacids3(item, group_indices=group_indices, check=False)


def to_string_aminoacids1(item, molecular_system, atom_indices='all', structure_indices='all'):

	from molsysmt.item.molsysmt_Topology import to_string_aminoacids1 as molsysmt_Topology_to_string_aminoacids1


	from molsysmt.item.molsysmt_Topology import get_group_index_from_atom as get_group_index_from_atom_molsysmt_Topology

	group_indices = get_group_index_from_atom_molsysmt_Topology(item, indices=atom_indices, check=False)
	group_indices = np.unique(group_indices)
	return molsysmt_Topology_to_string_aminoacids1(item, group_indices=group_indices, check=False)


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

	from molsysmt.item.molsysmt_Topology import to_openmm_Topology as molsysmt_Topology_to_openmm_Topology


	from molsysmt.basic import get

	box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)
	return molsysmt_Topology_to_openmm_Topology(item, box, atom_indices=atom_indices, check=False)


def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

	from molsysmt.item.molsysmt_Topology import to_mdtraj_Topology as molsysmt_Topology_to_mdtraj_Topology

	return molsysmt_Topology_to_mdtraj_Topology(item, atom_indices=atom_indices, check=False)


def to_pytraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

	from molsysmt.item.molsysmt_Topology import to_pytraj_Topology as molsysmt_Topology_to_pytraj_Topology

	return molsysmt_Topology_to_pytraj_Topology(item, atom_indices=atom_indices, check=False)


def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

	from molsysmt.item.molsysmt_Topology import to_file_pdb as molsysmt_Topology_to_file_pdb


	from molsysmt.basic import get

	coordinates = get(molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices, coordinates=True)
	box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)
	return molsysmt_Topology_to_file_pdb(item, coordinates, box, atom_indices=atom_indices, output_filename=output_filename, check=False)


def to_string_pdb_text(item, molecular_system, atom_indices='all', structure_indices='all'):

	from molsysmt.item.molsysmt_Topology import to_string_pdb_text as molsysmt_Topology_to_string_pdb_text


	from molsysmt.basic import get

	coordinates = get(molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices, coordinates=True)
	box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)
	return molsysmt_Topology_to_string_pdb_text(item, coordinates=coordinates, box=box, atom_indices=atom_indices, check=False)


