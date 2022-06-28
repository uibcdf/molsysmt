from molsysmt._private.exceptions import *

from molsysmt.item.file_gro.is_file_gro import is_file_gro as is_form
from molsysmt.item.file_gro.extract import extract
from molsysmt.item.file_gro.add import add
from molsysmt.item.file_gro.append_structures import append_structures
from molsysmt.item.file_gro.get import *
from molsysmt.item.file_gro.set import *
from .form_attributes import form_attributes

form_name = 'file:gro'
form_type = 'file'
form_info = ["Gromacs gro file format",
             "http://manual.gromacs.org/documentation/2018/user-guide/file-formats.html#gro"]


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
form_attributes['chain_index'] = True
form_attributes['chain_id'] = True
form_attributes['chain_name'] = True
form_attributes['chain_type'] = True
form_attributes['coordinates'] = True
form_attributes['velocities'] = True
form_attributes['box'] = True


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_gro import to_molsysmt_MolSys as file_gro_to_molsysmt_MolSys

    return file_gro_to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                          structure_indices=structure_indices, check=False)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_gro import to_molsysmt_Topology as file_gro_to_molsysmt_Topology

    return file_gro_to_molsysmt_Topology(item, atom_indices=atom_indices, check=False)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_gro import to_molsysmt_Structures as file_gro_to_molsysmt_Structures

    return file_gro_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                               structure_indices=structure_indices, check=False)


def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_gro import to_mdtraj_Trajectory as file_gro_to_mdtraj_Trajectory

    return file_gro_to_mdtraj_Trajectory(item, atom_indices=atom_indices,
                                             structure_indices=structure_indices, check=False)


def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_gro import to_mdtraj_Topology as file_gro_to_mdtraj_Topology

    tmp_item = file_gro_to_mdtraj_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item


def to_mdtraj_GroTrajectoryFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_gro import to_mdtraj_GroTrajectoryFile as file_gro_to_mdtraj_GroTrajectoryFile

    return file_gro_to_mdtraj_GroTrajectoryFile(item, atom_indices=atom_indices,
            structure_indices=structure_indices, check=False)


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_gro import to_openmm_Topology as file_gro_to_openmm_Topology

    return file_gro_to_openmm_Topology(item, atom_indices=atom_indices, check=False)


def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_gro import to_openmm_Modeller as file_gro_to_openmm_Modeller

    return file_gro_to_openmm_Modeller(item, atom_indices=atom_indices,
                                       structure_indices=structure_indices, check=False)


def to_openmm_GromacsGroFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_gro import to_openmm_GromacsGroFile as file_gro_to_openmm_GromacsGroFile

    return file_gro_to_openmm_GromacsGroFile(item, atom_indices=atom_indices,
                                             structure_indices=structure_indices, check=False)


def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_gro import to_nglview_NGLWidget as file_gro_to_nglview_NGLWidget

    return file_gro_to_nglview_NGLWidget(item, atom_indices=atom_indices,
                                         structure_indices=structure_indices, check=False)
