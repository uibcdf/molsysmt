from molsysmt.form.mdtraj_DCDTrajectoryFile.is_mdtraj_DCDTrajectoryFile import is_mdtraj_DCDTrajectoryFile as is_form
from molsysmt.form.mdtraj_DCDTrajectoryFile.extract import extract
from molsysmt.form.mdtraj_DCDTrajectoryFile.add import add
from molsysmt.form.mdtraj_DCDTrajectoryFile.append_structures import append_structures
from molsysmt.form.mdtraj_DCDTrajectoryFile.get import *
from molsysmt.form.mdtraj_DCDTrajectoryFile.set import *
from molsysmt.form.mdtraj_DCDTrajectoryFile.iterators import StructuresIterator, TopologyIterator
from .form_attributes import form_attributes

form_name = 'mdtraj.DCDTrajectoryFile'
form_type = 'class'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['coordinates'] = True
form_attributes['box'] = True
form_attributes['time'] = True
form_attributes['step'] = True

def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_DCDTrajectoryFile import \
        to_molsysmt_Structures as mdtraj_DCDTrajectoryFile_to_molsysmt_Structures

    return mdtraj_DCDTrajectoryFile_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                           structure_indices=structure_indices)

