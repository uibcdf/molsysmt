from molsysmt._private.exceptions import *

from molsysmt.form.openmm_PDBFile.is_openmm_PDBFile import is_openmm_PDBFile as is_form
from molsysmt.form.openmm_PDBFile.extract import extract
from molsysmt.form.openmm_PDBFile.add import add
from molsysmt.form.openmm_PDBFile.merge import merge
from molsysmt.form.openmm_PDBFile.append_structures import append_structures
from molsysmt.form.openmm_PDBFile.concatenate_structures import concatenate_structures
from molsysmt.form.openmm_PDBFile.get import *
from molsysmt.form.openmm_PDBFile.set import *

form_name='openmm.PDBFile'
form_type='class'
form_info=["",""]

form_attributes = {

    'atom_index' : True,
    'atom_id' : True,
    'atom_name' : True,
    'atom_type' : True,

    'bond_index' : False,
    'bond_id' : False,
    'bond_name' : False,
    'bond_type' : False,

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
    'velocities' : False,
    'box' : True,
    'time' : True,
    'step' : True,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,

}

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_PDBFile import to_molsysmt_Topology as openmm_PDBFile_to_molsysmt_Topology

    tmp_item = openmm_PDBFile_to_molsysmt_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_PDBFile import to_molsysmt_Structures as openmm_PDBFile_to_molsysmt_Structures

    tmp_item = openmm_PDBFile_to_molsysmt_Structures(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_PDBFile import to_molsysmt_MolSys as openmm_PDBFile_to_molsysmt_MolSys

    tmp_item = openmm_PDBFile_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_PDBFile import to_mdtraj_Trajectory as openmm_PDBFile_to_mdtraj_Trajectory

    tmp_item = openmm_PDBFile_to_molsysmt_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_PDBFile import to_mdtraj_Topology as openmm_PDBFile_to_mdtraj_Topology

    tmp_item = openmm_PDBFile_to_mdtraj_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_Topology import to_openmm_Topology as openmm_PDBFile_to_mdtraj_Topology

    tmp_item = openmm_PDBFile_to_mdtraj_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_Topology import to_nglview_NGLWidget as openmm_Topology_to_nglview_NGLWidget

    tmp_item = openmm_Topology_to_nglview_NGLWidget(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item


