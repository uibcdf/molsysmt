from molsysmt.form.molsysmt_Structures.is_molsysmt_Structures import is_molsysmt_Structures as is_form
from molsysmt.form.molsysmt_Structures.extract import extract
from molsysmt.form.molsysmt_Structures.add import add
from molsysmt.form.molsysmt_Structures.append_structures import append_structures
from molsysmt.form.molsysmt_Structures.get import *
from molsysmt.form.molsysmt_Structures.set import *
from molsysmt.form.molsysmt_Structures.iterators import StructuresIterator, TopologyIterator
from .form_attributes import form_attributes

form_name = 'molsysmt.Structures'
form_type = 'class'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['coordinates'] = True
form_attributes['box'] = True
form_attributes['time'] = True
form_attributes['step'] = True


# Methods
def to_molsysmt_TrajectoryDict(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_Structures import \
        to_molsysmt_TrajectoryDict as molsysmt_Structures_to_molsysmt_TrajectoryDict

    return molsysmt_Structures_to_molsysmt_TrajectoryDict(item, atom_indices=atom_indices,
                                                          structure_indices=structure_indices)


def to_XYZ(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_Structures import to_XYZ as molsysmt_Structures_to_XYZ

    return molsysmt_Structures_to_XYZ(item, atom_indices=atom_indices, structure_indices=structure_indices)
