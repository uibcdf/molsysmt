from molsysmt._private.exceptions import *

from molsysmt.form.mdtraj_HDF5TrajectoryFile.is_mdtraj_HDF5TrajectoryFile import is_mdtraj_HDF5TrajectoryFile as is_form
from molsysmt.form.mdtraj_HDF5TrajectoryFile.extract import extract
from molsysmt.form.mdtraj_HDF5TrajectoryFile.add import add
from molsysmt.form.mdtraj_HDF5TrajectoryFile.append_structures import append_structures
from molsysmt.form.mdtraj_HDF5TrajectoryFile.get import *
from molsysmt.form.mdtraj_HDF5TrajectoryFile.set import *

form_name='mdtraj.HDF5TrajectoryFile'
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
    'velocities' : True,
    'box' : True,
    'time' : True,
    'step' : True,

    'forcefield_parameters' : True,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.mdtraj_HDF5TrajectoryFile import to_mdtraj_Topology as mdtraj_HDF5TrajectoryFile_to_mdtraj_Topology

    tmp_item = mdtraj_HDF5TrajectoryFile_to_mdtraj_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.mdtraj_HDF5TrajectoryFile import to_openmm_Topology as mdtraj_HDF5TrajectoryFile_to_openmm_Topology

    tmp_item = mdtraj_HDF5TrajectoryFile_to_openmm_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.mdtraj_HDF5TrajectoryFile import to_molsysmt_MolSys as mdtraj_HDF5TrajectoryFile_to_molsysmt_MolSys

    tmp_item = mdtraj_HDF5TrajectoryFile_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.mdtraj_HDF5TrajectoryFile import to_molsysmt_Topology as mdtraj_HDF5TrajectoryFile_to_molsysmt_Topology

    tmp_item = mdtraj_HDF5TrajectoryFile_to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.mdtraj_HDF5TrajectoryFile import to_molsysmt_Structures as mdtraj_HDF5TrajectoryFile_to_molsysmt_Structures

    tmp_item = mdtraj_HDF5TrajectoryFile_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

