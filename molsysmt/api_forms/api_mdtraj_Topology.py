from molsysmt._private.exceptions import *

from molsysmt.form.mdtraj_Topology.is_mdtraj_Topology import is_mdtraj_Topology as is_form
from molsysmt.form.mdtraj_Topology.extract import extract
from molsysmt.form.mdtraj_Topology.add import add
from molsysmt.form.mdtraj_Topology.append_structures import append_structures
from molsysmt.form.mdtraj_Topology.get import *
from molsysmt.form.mdtraj_Topology.set import *

form_name='mdtraj.Topology'
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

    'entity_index' : False,
    'entity_id' : False,
    'entity_name' : False,
    'entity_type' : False,

    'coordinates' : False,
    'velocities' : False,
    'box' : False,
    'time' : False,
    'step' : False,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}


## To other form

def to_string_aminoacids3(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.mdtraj_Topology import to_string_aminoacids3 as mdtraj_Topology_to_string_aminoacids3
    from molsysmt.form.mdtraj_Topology import get_group_index_from_atom

    group_indices = get_group_index_from_atom(item, indices=atom_indices, check=False)
    tmp_item = mdtraj_Topology_to_string_aminoacids3(item, group_indices=group_indices, check=False)

    return tmp_item

def to_string_aminoacids1(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.mdtraj_Topology import to_string_aminoacids1 as mdtraj_Topology_to_string_aminoacids1
    from molsysmt.form.mdtraj_Topology import get_group_index_from_atom

    group_indices = get_group_index_from_atom(item, indices=atom_indices, check=False)
    tmp_item = mdtraj_Topology_to_string_aminoacids1(item, group_indices=group_indices, check=False)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.mdtraj_Topology import to_molsysmt_Topology as mdtraj_Topology_to_molsysmt_Topology

    tmp_item = mdtraj_Topology_to_molsysmt_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.mdtraj_Topology import to_openmm_Topology as mdtraj_Topology_to_openmm_Topology

    tmp_item = mdtraj_Topology_to_openmm_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_parmed_Structure(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.mdtraj_Topology import to_parmed_Structure as mdtraj_Topology_to_parmed_Structure

    tmp_item = mdtraj_Topology_to_parmed_Structure(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_parmed_GromacsTopologyFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.mdtraj_Topology import to_parmed_Structure as mdtraj_Topology_to_parmed_Structure

    tmp_item = mdtraj_Topology_to_parmed_Structure(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_file_top(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.form.mdtraj_Topology import to_file_top as mdtraj_Topology_to_file_top

    tmp_item = mdtraj_Topology_to_parmed_Structure(item, atom_indices=atom_indices, output_filename=output_filename, check=False)

    return tmp_item

def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.mdtraj_Topology import to_mdtraj_Trajectory as mdtraj_Topology_to_mdtraj_Trajectory
    from molsysmt.basic import get

    coordinates = get(molecular_system, target='atom', selection=atom_indices,
            structure_indices=structure_indices, coordinates=True, check=False)
    box = get(molecular_system, target='system', structure_indices=structure_indices, box=True,
            check=False)

    tmp_item = mdtraj_Topology_to_mdtraj_Trajectory(item, atom_indices=atom_indices,
            coordinates=coordinates, box=box, check=False)

    return tmp_item


