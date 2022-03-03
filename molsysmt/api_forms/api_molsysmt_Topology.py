from molsysmt._private_tools.exceptions import *

from molsysmt.tools.molsysmt_Topology.is_molsysmt_Topology import is_molsysmt_Topology as is_form
from molsysmt.tools.molsysmt_Topology.extract import extract
from molsysmt.tools.molsysmt_Topology.add import add
from molsysmt.tools.molsysmt_Topology.merge import merge
from molsysmt.tools.molsysmt_Topology.append_structures import append_structures
from molsysmt.tools.molsysmt_Topology.concatenate_structures import concatenate_structures
from molsysmt.tools.molsysmt_Topology.get import *
from molsysmt.tools.molsysmt_Topology.set import *

form_name='molsysmt.Topology'
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

    'group_index' : True,
    'group_id' : True,
    'group_name' : True,
    'group_type' : True,

    'component_index' : True,
    'component_id' : True,
    'component_name' : True,
    'component_type' : True,

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
    'box' : False,
    'time' : False,
    'step' : False,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}

def to_string_aminoacids3(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.molsysmt_Topology import to_string_aminoacids3 as molsysmt_Topology_to_string_aminoacids3

    tmp_item = molsysmt_Topology_to_string_aminoacids3(item, atom_indices=atom_indices, check_form=False)

    return tmp_item

def to_string_aminoacids1(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.molsysmt_Topology import to_string_aminoacids1 as molsysmt_Topology_to_string_aminoacids1

    tmp_item = molsysmt_Topology_to_string_aminoacids1(item, atom_indices=atom_indices, check_form=False)

    return tmp_item

def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.molsysmt_Topology import to_openmm_Topology as molsysmt_Topology_to_openmm_Topology
    from molsysmt.basic import get

    box = get(molecular_system, target='system', structure_indices=structure_indices, box=True)

    tmp_item = molsysmt_Topology_to_openmm_Topology(item, box, atom_indices=atom_indices, check_form=False)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.molsysmt_Topology import to_mdtraj_Topology as molsysmt_Topology_to_mdtraj_Topology

    tmp_item = molsysmt_Topology_to_mdtraj_Topology(item, atom_indices=atom_indices, check_form=False)

    return tmp_item

def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.tools.molsysmt_Topology import to_file_pdb as molsysmt_Topology_to_file_pdb
    from molsysmt.basic import get

    coordinates = get(molecular_system, target='atom', selection=atom_indices, structure_indices=structure_indices, coordinates=True)
    box = get(molecular_system, target='system', structure_indices=structure_indices, box=True)

    tmp_item = molsysmt_Topology_to_file_pdb(item, coordinates, box, atom_indices=atom_indices, output_filename=output_filename, check_form=False)

    return tmp_item

def to_string_pdb_text(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.molsysmt_Topology import to_string_pdb_text as molsysmt_Topology_to_string_pdb_text
    from molsysmt.basic import get

    coordinates = get(molecular_system, target='atom', selection=atom_indices, structure_indices=structure_indices, coordinates=True)
    box = get(molecular_system, target='system', structure_indices=structure_indices, box=True)

    tmp_item = molsysmt_Topology_to_string_pdb_text(item, coordinates, box, atom_indices=atom_indices, output_filename=output_filename, check_form=False)

    return tmp_item

