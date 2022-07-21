from molsysmt.item.file_xyznpy.is_file_xyznpy import is_file_xyznpy as is_form
from molsysmt.item.file_xyznpy.extract import extract
from molsysmt.item.file_xyznpy.add import add
from molsysmt.item.file_xyznpy.append_structures import append_structures
from molsysmt.item.file_xyznpy.get import *
from molsysmt.item.file_xyznpy.set import *
from .form_attributes import form_attributes

form_name = 'file:xyznpy'
form_type = 'file'
form_info = ["XYZ file format like saved with Numpy", ""]

form_attributes = form_attributes()
form_attributes['coordinates'] = True


def to_XYZ(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.file_xyznpy import to_XYZ as file_xyznpy_to_XYZ

    return file_xyznpy_to_XYZ(item, atom_indices=atom_indices, structure_indices=structure_indices)
