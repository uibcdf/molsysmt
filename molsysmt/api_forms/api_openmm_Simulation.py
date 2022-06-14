from molsysmt._private.exceptions import *

from molsysmt.item.openmm_Simulation.is_openmm_Simulation import is_openmm_Simulation as is_form
from molsysmt.item.openmm_Simulation.extract import extract
from molsysmt.item.openmm_Simulation.add import add
from molsysmt.item.openmm_Simulation.append_structures import append_structures
from molsysmt.item.openmm_Simulation.get import *
from molsysmt.item.openmm_Simulation.set import *

form_name='openmm.Simulation'
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

    'coordinates' : True,
    'velocities' : True,
    'box' : True,
    'time' : True,
    'step' : True,

    'forcefield' : True,
    'temperature' : True,
    'pressure' : True,
    'integrator' : True,
    'damping' : True,
}


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.openmm_Simulation import to_molsysmt_Topology as openmm_Simulation_to_molsysmt_Topology

    tmp_item = openmm_Simulation_to_molsysmt_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.openmm_Simulation import to_molsysmt_Structures as openmm_Simulation_to_molsysmt_Structures

    tmp_item = openmm_Simulation_to_molsysmt_Structures(item, atom_indices=atom_indices,
            structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.openmm_Simulation import to_molsysmt_MolSys as openmm_Simulation_to_molsysmt_MolSys

    tmp_item = openmm_Simulation_to_molsysmt_MolSys(item, atom_indices=atom_indices,
            structure_indices=structure_indices, check=False)

    return tmp_item

def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.openmm_Simulation import to_openmm_Topology as openmm_Simulation_to_openmm_Topology

    tmp_item = openmm_Simulation_to_openmm_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.openmm_Simulation import to_openmm_Modeller as openmm_Simulation_to_openmm_Modeller

    tmp_item = openmm_Simulation_to_openmm_Modeller(item, atom_indices=atom_indices,
            structure_indices=structure_indices, check=False)

    return tmp_item

def to_openmm_Context(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.openmm_Simulation import to_openmm_Context as openmm_Simulation_to_openmm_Context

    tmp_item = openmm_Simulation_to_openmm_Context(item, atom_indices=atom_indices,
            structure_indices=structure_indices, check=False)

    return tmp_item

def to_pdbfixer_PDBFixer(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.openmm_Simulation import to_pdbfixer_PDBFixer as openmm_Simulation_to_pdbfixer_PDBFixer

    tmp_item = openmm_Simulation_to_pdbfixer_PDBFixer(item, atom_indices=atom_indices,
            structure_indices=structure_indices, check=False)

    return tmp_item

def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.item.openmm_Simulation import to_file_pdb as openmm_Simulation_to_file_pdb

    tmp_item = openmm_Simulation_to_file_pdb(item, atom_indices=atom_indices,
            structure_indices=structure_indices, output_filename=output_filename, check=False)

    return tmp_item


