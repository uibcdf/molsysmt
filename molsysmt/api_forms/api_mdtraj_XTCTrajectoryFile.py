from molsysmt.form.mdtraj_XTCTrajectoryFile.is_mdtraj_XTCTrajectoryFile import is_mdtraj_XTCTrajectoryFile as is_form
from molsysmt.form.mdtraj_XTCTrajectoryFile.extract import extract
from molsysmt.form.mdtraj_XTCTrajectoryFile.add import add
from molsysmt.form.mdtraj_XTCTrajectoryFile.append_structures import append_structures
from molsysmt.form.mdtraj_XTCTrajectoryFile.get import *
from molsysmt.form.mdtraj_XTCTrajectoryFile.set import *
from molsysmt.form.mdtraj_XTCTrajectoryFile.iterators import StructuresIterator, TopologyIterator
from .form_attributes import form_attributes

form_name = 'mdtraj.XTCTrajectoryFile'
form_type = 'class'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['coordinates'] = True
form_attributes['box'] = True
form_attributes['time'] = True
form_attributes['structure_id'] = True


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_XTCTrajectoryFile import \
        to_molsysmt_Structures as mdtraj_XTCTrajectoryFile_to_molsysmt_Structures

    return mdtraj_XTCTrajectoryFile_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                           structure_indices=structure_indices,
                                                           )
