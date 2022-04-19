from molsysmt._private.exceptions import *

from molsysmt.form.file_h5.is_file_h5 import is_file_h5 as is_form
from molsysmt.form.file_h5.extract import extract
from molsysmt.form.file_h5.add import add
from molsysmt.form.file_h5.append_structures import append_structures
from molsysmt.form.file_h5.get import *
from molsysmt.form.file_h5.set import *

form_name='file:h5'
form_type='file'
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


def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_h5 import to_mdtraj_Trajectory as file_h5_to_mdtraj_Trajectory

    tmp_item = file_h5_to_mdtraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_h5 import to_mdtraj_Topology as file_h5_to_mdtraj_Topology

    tmp_item = file_h5_to_mdtraj_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_mdtraj_HDF5TrajectoryFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_h5 import to_mdtraj_HDF5TrajectoryFile as file_h5_to_mdtraj_HDF5TrajectoryFile

    tmp_item = file_h5_to_mdtraj_HDF5TrajectoryFile(item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices, check=False)

    return tmp_item

def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_h5 import to_openmm_Topology as file_h5_to_openmm_Topology

    tmp_item = file_h5_to_openmm_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_h5 import to_molsysmt_MolSys as file_h5_to_molsysmt_MolSys

    tmp_item = file_h5_to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                          structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system=None, atom_indices='all'):

    from molsysmt.form.file_h5 import to_molsysmt_Topology as file_h5_to_molsysmt_Topology

    tmp_item = file_h5_to_molsysmt_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_molsysmt_Structures(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_h5 import to_molsysmt_Structures as file_h5_to_molsysmt_Structures

    tmp_item = file_h5_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                          structure_indices=structure_indices, check=False)

    return tmp_item

def to_file_pdb(item, molecular_system=None, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.form.file_h5 import to_file_pdb as file_h5_to_file_pdb

    tmp_item = file_h5_to_file_pdb(item, atom_indices=atom_indices,
                                   structure_indices=structure_indices,
                                   output_filename=output_filename, check=False)

    return tmp_item

def to_nglview_NGLWidget(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_h5 import to_nglview_NGLWidget as file_h5_to_nglview_NGLWidget

    tmp_item = file_h5_to_nglview_NGLWidget(item, atom_indices=atom_indices,
                                   structure_indices=structure_indices, check=False)

    return tmp_item

