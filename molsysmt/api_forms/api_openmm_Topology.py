from molsysmt._private.exceptions import *

from molsysmt.form.openmm_Topology.is_openmm_Topology import is_openmm_Topology as is_form
from molsysmt.form.openmm_Topology.extract import extract
from molsysmt.form.openmm_Topology.add import add
from molsysmt.form.openmm_Topology.append_structures import append_structures
from molsysmt.form.openmm_Topology.get import *
from molsysmt.form.openmm_Topology.set import *

form_name='openmm.Topology'
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
    'box' : True,
    'time' : False,
    'step' : False,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}


def to_molsysmt_Topology(item, molecular_system, atom_indices='all'):

    from molsysmt.form.openmm_Topology import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology

    tmp_item = openmm_Topology_to_molsysmt_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_Topology import to_molsysmt_MolSys as openmm_Topology_to_molsysmt_MolSys
    from molsysmt.basic import get

    coordinates, box = get(molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, coordinates=True, box=True)

    tmp_item = openmm_Topology_to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                                  coordinates=coordinates, box=box, check=False)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_Topology import to_mdtraj_Topology as openmm_Topology_to_mdtraj_Topology

    tmp_item = openmm_Topology_to_mdtraj_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_parmed_Structure(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_Topology import to_parmed_Structure as openmm_Topology_to_parmed_Structure

    tmp_item = openmm_Topology_to_parmed_Structure(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_Topology import to_openmm_Modeller as openmm_Topology_to_openmm_Modeller
    from molsysmt.basic import get

    coordinates = get(molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, coordinates=True)

    tmp_item = openmm_Topology_to_openmm_Modeller(item, atom_indices=atom_indices, coordinates=coordinates, check=False)

    return tmp_item

def to_openmm_System(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_Topology import to_openmm_System as openmm_Topology_to_openmm_System
    from molsysmt.basic import convert

    molecular_mechanics = convert(molecular_system, to_form='molsysmt.MolecularMechanics')

    forcefield = molecular_mechanics.to_openmm_ForceField()
    system_parameters = molecular_mechanics.get_openmm_System_parameters()

    tmp_item = openmm_Topology_to_openmm_System(item, atom_indices=atom_indices,
                                                forcefield=forcefield, parameters=parameters,
                                                check=False)

    return tmp_item

def to_openmm_Context(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_Topology import to_openmm_Context as openmm_Topology_to_openmm_Context
    from molsysmt.basic import convert

    molecular_mechanics = convert(molecular_system, to_form='molsysmt.MolecularMechanics')

    forcefield = molecular_mechanics.to_openmm_ForceField()
    system_parameters = molecular_mechanics.get_openmm_System_parameters()

    tmp_item = openmm_Topology_to_openmm_Context(item, atom_indices=atom_indices,
                                                forcefield=forcefield, parameters=parameters,
                                                check=False)

    return tmp_item

def to_openmm_Simulation(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_Topology import to_openmm_Simulation as openmm_Topology_to_openmm_Simulation
    from molsysmt.basic import convert

    molecular_mechanics = convert(molecular_system, to_form='molsysmt.MolecularMechanics')

    forcefield = molecular_mechanics.to_openmm_ForceField()
    system_parameters = molecular_mechanics.get_openmm_System_parameters()

    tmp_item = openmm_Topology_to_openmm_Context(item, atom_indices=atom_indices,
                                                forcefield=forcefield, parameters=parameters,
                                                check=False)

    return tmp_item

def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.form.openmm_Topology import to_file_pdb as openmm_Topology_to_file_pdb
    from molsysmt.basic import get

    coordinates = get(molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, coordinates=True)

    tmp_item = openmm_Topology_to_file_pdb(item, atom_indices=atom_indices, coordinates=coordinates, check=False)

    return tmp_item

def to_string_pdb_text(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_Topology import to_string_pdb_text as openmm_Topology_to_string_pdb_text
    from molsysmt.basic import get

    coordinates = get(molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, coordinates=True)

    tmp_item = openmm_Topology_to_file_pdb(item, atom_indices=atom_indices, coordinates=coordinates, check=False)

    return tmp_item

def to_openmm_PDBFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_Topology import to_openmm_PDBFile as openmm_Topology_to_openmm_PDBFile
    from molsysmt.basic import get

    coordinates = get(molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, coordinates=True)

    tmp_item = openmm_Topology_to_openmm_PDBFile(item, atom_indices=atom_indices, coordinates=coordinates, check=False)

    return tmp_item

def to_nglview_NGLWidget(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_Topology import to_nglview_NGLWidget as openmm_Topology_to_nglview_NGLWidget
    from molsysmt.basic import get

    coordinates = get(molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, coordinates=True)

    tmp_item = openmm_Topology_to_nglview_NGLWidget(item, atom_indices=atom_indices, coordinates=coordinates, check=False)

    return tmp_item


