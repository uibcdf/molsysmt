from molsysmt.form.file_dcd.is_file_dcd import is_file_dcd as is_form
from molsysmt.form.file_dcd.extract import extract
from molsysmt.form.file_dcd.add import add
from molsysmt.form.file_dcd.append_structures import append_structures
from molsysmt.form.file_dcd.get import *
from molsysmt.form.file_dcd.set import *
from molsysmt.form.file_dcd.iterators import StructuresIterator, TopologyIterator
from .form_attributes import form_attributes

form_name = 'file:dcd'
form_type = 'file'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['coordinates'] = True
form_attributes['box'] = True

def to_mdtraj_DCDTrajectoryFile(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_dcd import to_mdtraj_DCDTrajectoryFile as file_xtc_to_mdtraj_DCDTrajectoryFile

    return file_xtc_to_mdtraj_DCDTrajectoryFile(item, atom_indices=atom_indices, structure_indices=structure_indices)


