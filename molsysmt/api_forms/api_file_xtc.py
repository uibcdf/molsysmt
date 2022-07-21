from molsysmt.item.file_xtc.is_file_xtc import is_file_xtc as is_form
from molsysmt.item.file_xtc.extract import extract
from molsysmt.item.file_xtc.add import add
from molsysmt.item.file_xtc.append_structures import append_structures
from molsysmt.item.file_xtc.get import *
from molsysmt.item.file_xtc.set import *
from .form_attributes import form_attributes

form_name = 'file:xtc'
form_type = 'file'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['coordinates'] = True
form_attributes['box'] = True
form_attributes['time'] = True
form_attributes['step'] = True


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.file_xtc import to_molsysmt_Structures as file_xtc_to_molsysmt_Structures

    return file_xtc_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_mdtraj_XTCTrajectoryFile(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.file_xtc import to_mdtraj_XTCTrajectoryFile as file_xtc_to_mdtraj_XTCTrajectoryFile

    return file_xtc_to_mdtraj_XTCTrajectoryFile(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.file_xtc import to_mdtraj_Trajectory as file_xtc_to_mdtraj_Trajectory

    return file_xtc_to_mdtraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices)
