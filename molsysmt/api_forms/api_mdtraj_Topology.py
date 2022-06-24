from molsysmt._private.exceptions import *
from molsysmt.item.mdtraj_Topology.is_mdtraj_Topology import is_mdtraj_Topology as is_form
from molsysmt.item.mdtraj_Topology.extract import extract
from molsysmt.item.mdtraj_Topology.add import add
from molsysmt.item.mdtraj_Topology.append_structures import append_structures
from molsysmt.item.mdtraj_Topology.get import *
from molsysmt.item.mdtraj_Topology.set import *
from .form_attributes import form_attributes

form_name = 'mdtraj.Topology'
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
form_attributes['component_index'] = True
form_attributes['molecule_index'] = True
form_attributes['molecule_id'] = True
form_attributes['molecule_name'] = True
form_attributes['molecule_type'] = True
form_attributes['chain_index'] = True
form_attributes['chain_id'] = True
form_attributes['chain_name'] = True
form_attributes['chain_type'] = True


	## To other form
def to_string_aminoacids3(item, molecular_system, atom_indices='all', structure_indices='all'):

	from molsysmt.item.mdtraj_Topology import to_string_aminoacids3 as mdtraj_Topology_to_string_aminoacids3


	from molsysmt.item.mdtraj_Topology import get_group_index_from_atom

	group_indices = get_group_index_from_atom(item, indices=atom_indices, check=False)
	return mdtraj_Topology_to_string_aminoacids3(item, group_indices=group_indices, check=False)


def to_string_aminoacids1(item, molecular_system, atom_indices='all', structure_indices='all'):

	from molsysmt.item.mdtraj_Topology import to_string_aminoacids1 as mdtraj_Topology_to_string_aminoacids1


	from molsysmt.item.mdtraj_Topology import get_group_index_from_atom

	group_indices = get_group_index_from_atom(item, indices=atom_indices, check=False)
	return mdtraj_Topology_to_string_aminoacids1(item, group_indices=group_indices, check=False)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

	from molsysmt.item.mdtraj_Topology import to_molsysmt_Topology as mdtraj_Topology_to_molsysmt_Topology

	return mdtraj_Topology_to_molsysmt_Topology(item, atom_indices=atom_indices, check=False)


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

	from molsysmt.item.mdtraj_Topology import to_openmm_Topology as mdtraj_Topology_to_openmm_Topology

	return mdtraj_Topology_to_openmm_Topology(item, atom_indices=atom_indices, check=False)


def to_parmed_Structure(item, molecular_system, atom_indices='all', structure_indices='all'):

	from molsysmt.item.mdtraj_Topology import to_parmed_Structure as mdtraj_Topology_to_parmed_Structure

	return mdtraj_Topology_to_parmed_Structure(item, atom_indices=atom_indices, check=False)


def to_parmed_GromacsTopologyFile(item, molecular_system, atom_indices='all', structure_indices='all'):

	from molsysmt.item.mdtraj_Topology import to_parmed_Structure as mdtraj_Topology_to_parmed_Structure

	return mdtraj_Topology_to_parmed_Structure(item, atom_indices=atom_indices, check=False)


def to_file_top(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

	from molsysmt.item.mdtraj_Topology import to_file_top as mdtraj_Topology_to_file_top

	return mdtraj_Topology_to_parmed_Structure(item, atom_indices=atom_indices, output_filename=output_filename, check=False)


def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):

	from molsysmt.item.mdtraj_Topology import to_mdtraj_Trajectory as mdtraj_Topology_to_mdtraj_Trajectory


	from molsysmt.basic import get

	coordinates = get(molecular_system, element='atom', selection=atom_indices,
	structure_indices=structure_indices, coordinates=True, check=False)
	box = get(molecular_system, element='system', structure_indices=structure_indices, box=True,
	check=False)
	return mdtraj_Topology_to_mdtraj_Trajectory(item, atom_indices=atom_indices,
                                               coordinates=coordinates, box=box, check=False)


