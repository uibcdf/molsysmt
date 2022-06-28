from molsysmt._private.exceptions import *
from molsysmt.item.XYZ.is_XYZ import is_XYZ as is_form
from molsysmt.item.XYZ.extract import extract
from molsysmt.item.XYZ.add import add
from molsysmt.item.XYZ.append_structures import append_structures
from molsysmt.item.XYZ.get import *
from molsysmt.item.XYZ.set import *
from .form_attributes import form_attributes

form_name = 'XYZ'
form_type = 'class'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['coordinates'] = True


def to_molsysmt_Structures(item, molecular_system=None, atom_indices='all', structure_indices='all'):
    from molsysmt.item.XYZ import to_molsysmt_Structures as XYZ_to_molsysmt_Structures

    return XYZ_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)


def to_file_xyznpy(item, molecular_system=None, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.item.XYZ import to_file_xyznpy as XYZ_to_file_xyznpy

    return XYZ_to_file_xyznpy(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)
