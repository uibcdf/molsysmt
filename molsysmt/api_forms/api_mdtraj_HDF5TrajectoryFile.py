from molsysmt.form.mdtraj_HDF5TrajectoryFile.is_mdtraj_HDF5TrajectoryFile import is_mdtraj_HDF5TrajectoryFile as is_form
from molsysmt.form.mdtraj_HDF5TrajectoryFile.extract import extract
from molsysmt.form.mdtraj_HDF5TrajectoryFile.add import add
from molsysmt.form.mdtraj_HDF5TrajectoryFile.append_structures import append_structures
from molsysmt.form.mdtraj_HDF5TrajectoryFile.get import *
from molsysmt.form.mdtraj_HDF5TrajectoryFile.set import *
from .form_attributes import form_attributes

form_name = 'mdtraj.HDF5TrajectoryFile'
form_type = 'class'
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


def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_HDF5TrajectoryFile import \
        to_mdtraj_Topology as mdtraj_HDF5TrajectoryFile_to_mdtraj_Topology

    return mdtraj_HDF5TrajectoryFile_to_mdtraj_Topology(item, atom_indices=atom_indices)


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_HDF5TrajectoryFile import \
        to_openmm_Topology as mdtraj_HDF5TrajectoryFile_to_openmm_Topology

    return mdtraj_HDF5TrajectoryFile_to_openmm_Topology(item, atom_indices=atom_indices)


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_HDF5TrajectoryFile import \
        to_molsysmt_MolSys as mdtraj_HDF5TrajectoryFile_to_molsysmt_MolSys

    return mdtraj_HDF5TrajectoryFile_to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                                        structure_indices=structure_indices)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_HDF5TrajectoryFile import \
        to_molsysmt_Topology as mdtraj_HDF5TrajectoryFile_to_molsysmt_Topology

    return mdtraj_HDF5TrajectoryFile_to_molsysmt_Topology(item, atom_indices=atom_indices,
                                                          structure_indices=structure_indices)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_HDF5TrajectoryFile import \
        to_molsysmt_Structures as mdtraj_HDF5TrajectoryFile_to_molsysmt_Structures

    return mdtraj_HDF5TrajectoryFile_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                            structure_indices=structure_indices)
