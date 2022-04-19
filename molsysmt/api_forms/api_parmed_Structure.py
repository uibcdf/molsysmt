from molsysmt._private.exceptions import *

from molsysmt.form.parmed_Structure.is_parmed_Structure import is_parmed_Structure as is_form
from molsysmt.form.parmed_Structure.extract import extract
from molsysmt.form.parmed_Structure.add import add
from molsysmt.form.parmed_Structure.append_structures import append_structures
from molsysmt.form.parmed_Structure.get import *
from molsysmt.form.parmed_Structure.set import *

form_name='parmed.Structure'
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

## Methods

def to_parmed_GromacsTopologyFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.parmed_Structure import to_parmed_GromacsTopologyFile as parmed_Structure_to_parmed_GromacsTopologyFile

    tmp_item = parmed_Structure_to_parmed_GromacsTopologyFile(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.parmed_Structure import to_openmm_Topology as parmed_Structure_to_openmm_Topology

    tmp_item = parmed_Structure_to_openmm_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_openmm_Modeller(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.form.parmed_Structure import to_openmm_Modeller as parmed_Structure_to_openmm_Modeller

    tmp_item = parmed_Structure_to_openmm_Modeller(item, atom_indices=atom_indices,
            structure_indices=structure_indices, check=False)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.form.parmed_Structure import to_mdtraj_Topology as parmed_Structure_to_mdtraj_Topology

    tmp_item = parmed_Structure_to_mdtraj_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_mdtraj_Trajectory(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.form.parmed_Structure import to_mdtraj_Trajectory as parmed_Structure_to_mdtraj_Trajectory

    tmp_item = parmed_Structure_to_mdtraj_Trajectory(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_nglview_NGLWidget(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.form.parmed_Structure import to_nglview_NGLWidget as parmed_Structure_to_nglview_NGLWidget

    tmp_item = parmed_Structure_to_nglview_NGLWidget(item, atom_indices=atom_indices,
            structure_indices=structure_indices, check=False)

    return tmp_item

def to_file_pdb(item, molecular_system=None, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.form.parmed_Structure import to_file_pdb as parmed_Structure_to_file_pdb

    tmp_item = parmed_Structure_to_file_pdb(item, atom_indices=atom_indices,
            structure_indices=structure_indices, output_filename=output_filename, check=False)

    return tmp_item

def to_file_mol2(item, molecular_system=None, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.form.parmed_Structure import to_file_mol2 as parmed_Structure_to_file_mol2

    tmp_item = parmed_Structure_to_file_mol2(item, atom_indices=atom_indices,
            structure_indices=structure_indices, output_filename=output_filename, check=False)

    return tmp_item


