from molsysmt._private.exceptions import *

from molsysmt.form.openmm_Modeller.is_openmm_Modeller import is_openmm_Modeller as is_form
from molsysmt.form.openmm_Modeller.extract import extract
from molsysmt.form.openmm_Modeller.add import add
from molsysmt.form.openmm_Modeller.merge import merge
from molsysmt.form.openmm_Modeller.append_structures import append_structures
from molsysmt.form.openmm_Modeller.concatenate_structures import concatenate_structures
from molsysmt.form.openmm_Modeller.get import *
from molsysmt.form.openmm_Modeller.set import *

form_name='openmm.Modeller'
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
    'bond_order' : False,

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

    'coordinates' : True,
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


def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_Modeller import to_mdtraj_Trajectory as openmm_Modeller_to_mdtraj_Trajectory

    tmp_item = openmm_Modeller_to_mdtraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_Modeller import to_mdtraj_Topology as openmm_Modeller_to_mdtraj_Topology

    tmp_item = openmm_Modeller_to_mdtraj_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_openmm_System(item, molecular_system, atom_indices='all', structure_indices='all',
                     forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm', constraints=None,
                     rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                     flexible_constraints=False):

    from molsysmt.form.openmm_Modeller import to_openmm_System as openmm_Modeller_to_openmm_System

    tmp_item = openmm_Modeller_to_openmm_System(item, atom_indices=atom_indices, structure_indices=structure_indices,
                     forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm', constraints=None,
                     rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                     flexible_constraints=False, check=False)

    return tmp_item


def to_openmm_Simulation(item, molecular_system, atom_indices='all', structure_indices='all',
                         forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm', constraints=None,
                         rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                         flexible_constraints=False, integrator='Langevin', temperature='300.0 K',
                         collisions_rate='1.0 1/ps', integration_timestep='2.0 fs', platform='CUDA'):

    from molsysmt.form.openmm_Modeller import to_openmm_Simulation as openmm_Modeller_to_openmm_Simulation

    tmp_item = openmm_Modeller_to_openmm_Simulation(item, atom_indices=atom_indices, structure_indices=structure_indices,
                         forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm', constraints=None,
                         rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                         flexible_constraints=False, integrator='Langevin', temperature='300.0 K',
                         collisions_rate='1.0 1/ps', integration_timestep='2.0 fs', platform='CUDA',
                         check=False)

    return tmp_item

def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_Modeller import to_openmm_Topology as openmm_Modeller_to_openmm_Topology

    tmp_item = openmm_Modeller_to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_pdbfixer_PDBFixer(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_Modeller import to_pdbfixer_PDBFixer as openmm_Modeller_to_pdbfixer_PDBFixer

    tmp_item = openmm_Modeller_to_pdbfixer_PDBFixer(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_Modeller import to_molsysmt_MolSys as openmm_Modeller_to_molsysmt_MolSys

    tmp_item = openmm_Modeller_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.form.openmm_Modeller import to_file_pdb as openmm_Modeller_to_file_pdb

    tmp_item = openmm_Modeller_to_file_pdb(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                           output_filename=output_filename, check=False)

    return tmp_item

def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_Modeller import to_nglview_NGLWidget as openmm_Modeller_to_nglview_NGLWidget

    tmp_item = openmm_Modeller_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item


