from molsysmt.form.file_inpcrd.is_file_inpcrd import is_file_inpcrd as is_form
from molsysmt.form.file_inpcrd.extract import extract
from molsysmt.form.file_inpcrd.add import add
from molsysmt.form.file_inpcrd.append_structures import append_structures
from molsysmt.form.file_inpcrd.get import *
from molsysmt.form.file_inpcrd.set import *
from molsysmt.form.file_inpcrd.iterators import StructuresIterator, TopologyIterator
from .form_attributes import form_attributes

form_name = 'file:inpcrd'
form_type = 'file'
form_info = ["AMBER ASCII restart/inpcrd file format",
             "https://ambermd.org/FileFormats.php#trajectory"]

form_attributes = form_attributes()
form_attributes['coordinates'] = True
form_attributes['box'] = True


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_inpcrd import to_molsysmt_Structures as file_inpcrd_to_molsysmt_Structures

    return file_inpcrd_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                              structure_indices=structure_indices)


def to_mdtraj_AmberRestartFile(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_inpcrd import to_mdtraj_AmberRestartFile as file_inpcrd_to_mdtraj_AmberRestartFile

    return file_inpcrd_to_mdtraj_AmberRestartFile(item, atom_indices=atom_indices,
                                                  structure_indices=structure_indices)


def to_openmm_AmberInpcrdFile(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_inpcrd import to_openmm_AmberInpcrdFile as file_inpcrd_to_openmm_AmberInpcrdFile

    return file_inpcrd_to_openmm_AmberInpcrdFile(item, atom_indices=atom_indices,
                                                 structure_indices=structure_indices)
