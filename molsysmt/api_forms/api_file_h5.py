from molsysmt.form.file_h5.is_file_h5 import is_file_h5 as is_form
from molsysmt.form.file_h5.extract import extract
from molsysmt.form.file_h5.add import add
from molsysmt.form.file_h5.append_structures import append_structures
from molsysmt.form.file_h5.get import *
from molsysmt.form.file_h5.set import *
from .form_attributes import form_attributes

form_name = 'file:h5'
form_type = 'file'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['atom_index'] = True
form_attributes['atom_id'] = True
form_attributes['atom_name'] = True
form_attributes['atom_type'] = True
form_attributes['bond_index'] = True
form_attributes['bond_id'] = True
form_attributes['bond_name'] = True
form_attributes['bond_type'] = True
form_attributes['bond_order'] = True
form_attributes['group_index'] = True
form_attributes['group_id'] = True
form_attributes['group_name'] = True
form_attributes['group_type'] = True
form_attributes['component_index'] = True
form_attributes['molecule_index'] = True
form_attributes['molecule_id'] = True
form_attributes['molecule_name'] = True
form_attributes['molecule_type'] = True
form_attributes['chain_index'] = True
form_attributes['chain_id'] = True
form_attributes['chain_name'] = True
form_attributes['chain_type'] = True
form_attributes['coordinates'] = True
form_attributes['velocities'] = True
form_attributes['box'] = True
form_attributes['time'] = True
form_attributes['step'] = True
form_attributes['forcefield_parameters'] = True


def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_h5 import to_mdtraj_Trajectory as file_h5_to_mdtraj_Trajectory

    tmp_item = file_h5_to_mdtraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_h5 import to_mdtraj_Topology as file_h5_to_mdtraj_Topology

    tmp_item = file_h5_to_mdtraj_Topology(item, atom_indices=atom_indices)

    return tmp_item

def to_mdtraj_HDF5TrajectoryFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_h5 import to_mdtraj_HDF5TrajectoryFile as file_h5_to_mdtraj_HDF5TrajectoryFile

    tmp_item = file_h5_to_mdtraj_HDF5TrajectoryFile(item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices)

    return tmp_item

def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_h5 import to_openmm_Topology as file_h5_to_openmm_Topology

    tmp_item = file_h5_to_openmm_Topology(item, atom_indices=atom_indices)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_h5 import to_molsysmt_MolSys as file_h5_to_molsysmt_MolSys

    tmp_item = file_h5_to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                          structure_indices=structure_indices)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_h5 import to_molsysmt_Topology as file_h5_to_molsysmt_Topology

    tmp_item = file_h5_to_molsysmt_Topology(item, atom_indices=atom_indices)

    return tmp_item

def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_h5 import to_molsysmt_Structures as file_h5_to_molsysmt_Structures

    tmp_item = file_h5_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                          structure_indices=structure_indices)

    return tmp_item

def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.form.file_h5 import to_file_pdb as file_h5_to_file_pdb

    tmp_item = file_h5_to_file_pdb(item, atom_indices=atom_indices,
                                   structure_indices=structure_indices,
                                   output_filename=output_filename)

    return tmp_item

def to_nglview_NGLWidget(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_h5 import to_nglview_NGLWidget as file_h5_to_nglview_NGLWidget

    tmp_item = file_h5_to_nglview_NGLWidget(item, atom_indices=atom_indices,
                                   structure_indices=structure_indices)

    return tmp_item

