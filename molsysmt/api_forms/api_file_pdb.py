from molsysmt._private.exceptions import *

from molsysmt.item.file_pdb.is_file_pdb import is_file_pdb as is_form
from molsysmt.item.file_pdb.extract import extract
from molsysmt.item.file_pdb.add import add
from molsysmt.item.file_pdb.append_structures import append_structures
from molsysmt.item.file_pdb.get import *
from molsysmt.item.file_pdb.set import *

form_name='file:pdb'
form_type='file'
form_info=["Protein Data Bank file format","https://www.rcsb.org/pdb/static.do?p=file_formats/pdb/index.html"]

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

    'forcefield_parameters' : True,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_pdb import to_molsysmt_MolSys as file_pdb_to_molsysmt_MolSys

    tmp_item = file_pdb_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_pdb import to_molsysmt_Topology as file_pdb_to_molsysmt_Topology

    tmp_item = file_pdb_to_molsysmt_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_pdb import to_molsysmt_Structures as file_pdb_to_molsysmt_Structures

    tmp_item = file_pdb_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_parmed_Structure(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_pdb import to_parmed_Structure as file_pdb_to_parmed_Structure

    tmp_item = file_pdb_to_parmed_Structure(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_mdanalysis_Universe(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_pdb import to_mdanalysis_Universe as file_pdb_to_mdanalysis_Universe

    tmp_item = file_pdb_to_mdanalysis_Universe(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item, tmp_molecular_system

def to_mdanalysis_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_pdb import to_mdanalysis_Topology as file_pdb_to_mdanalysis_Topology

    tmp_item = file_pdb_to_mdanalysis_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_mdanalysis_topology_PDBParser(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_pdb import to_mdanalysis_topology_PDBParser as file_pdb_to_mdanalysis_topology_PDBParser

    tmp_item = file_pdb_to_mdanalysis_topology_PDBParser(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_pdb import to_mdtraj_Topology as file_pdb_to_mdtraj_Topology

    tmp_item = file_pdb_to_mdtraj_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_pdb import to_mdtraj_Trajectory as file_pdb_to_mdtraj_Trajectory

    tmp_item = file_pdb_to_mdtraj_Trajectory(item, atom_indices=atom_indices,
            structure_indices=structure_indices, check=False)

    return tmp_item

def to_mdtraj_PDBTrajectoryFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_pdb import to_mdtraj_PDBTrajectoryFile as file_pdb_to_mdtraj_PDBTrajectoryFile

    tmp_item = file_pdb_to_mdtraj_PDBTrajectoryFile(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_file_mol2(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.item.file_pdb import to_file_mol2 as file_pdb_to_file_mol2

    tmp_item = file_pdb_to_file_mol2(item, atom_indices=atom_indices,
            structure_indices=structure_indices, output_filename=output_filename, check=False)

    return tmp_item

def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_pdb import to_openmm_Topology as file_pdb_to_openmm_Topology

    tmp_item = file_pdb_to_openmm_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_pdb import to_openmm_Modeller as file_pdb_to_openmm_Modeller

    tmp_item = file_pdb_to_openmm_Modeller(item, atom_indices=atom_indices,
            structure_indices=structure_indices, check=False)

    return tmp_item

def to_openmm_System(item, molecular_system, atom_indices='all', structure_indices='all',
                     forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm', constraints=None,
                     rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                     flexible_constraints=False):

    from molsysmt.item.file_pdb import to_openmm_System as file_pdb_to_openmm_System

    tmp_item = file_pdb_to_openmm_System(item, atom_indices=atom_indices, structure_indices=structure_indices,
                     forcefield=forcefield, non_bonded_method=non_bonded_method,
                     non_bonded_cutoff=non_bonded_cutoff, constraints=constraints,
                     rigid_water=rigid_water, remove_cm_motion=remove_cm_motion,
                     hydrogen_mass=hydrogen_mass, switch_distance=switch_distance,
                     flexible_constraints=flexible_constraints, check=False)

    return tmp_item


def to_openmm_Simulation(item, molecular_system, atom_indices='all', structure_indices='all',
                         forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff=None, constraints=None,
                         rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                         flexible_constraints=False, integrator='Langevin', temperature='300.0 K',
                         collisions_rate='1.0 1/ps', integration_timestep='2.0 fs', platform='CUDA'):

    from molsysmt.item.file_pdb import to_openmm_Simulation as file_pdb_to_openmm_Simulation

    tmp_item = file_pdb_to_openmm_Simulation(item, atom_indices=atom_indices, structure_indices=structure_indices,
                     forcefield=forcefield, non_bonded_method=non_bonded_method,
                     non_bonded_cutoff=non_bonded_cutoff, constraints=constraints,
                     rigid_water=rigid_water, remove_cm_motion=remove_cm_motion,
                     hydrogen_mass=hydrogen_mass, switch_distance=switch_distance,
                     flexible_constraints=flexible_constraints, integrator=integrator,
                     temperature=temperature, collisions_rate=collisions_rate,
                     integration_timestep=integration_timestep, platform=platform, check=False)

    return tmp_item

def to_openmm_PDBFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_pdb import to_openmm_PDBFile as file_pdb_to_openmm_PDBFile

    tmp_item = file_pdb_to_openmm_PDBFile(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_pdbfixer_PDBFixer(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_pdb import to_pdbfixer_PDBFixer as file_pdb_to_pdbfixer_PDBFixer

    tmp_item = file_pdb_to_pdbfixer_PDBFixer(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_pytraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_pdb import to_pytraj_Trajectory as file_pdb_to_pytraj_Trajectory

    tmp_item = file_pdb_to_pytraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_pytraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_pdb import to_pytraj_Topology as file_pdb_to_pytraj_Topology

    tmp_item = file_pdb_to_pytraj_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_pdb import to_nglview_NGLWidget as file_pdb_to_nglview_NGLWidget

    tmp_item = file_pdb_to_nglview_NGLWidget(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_string_pdb_text(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_pdb import to_string_pdb_text as file_pdb_to_string_pdb_text

    tmp_item = file_pdb_to_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item


