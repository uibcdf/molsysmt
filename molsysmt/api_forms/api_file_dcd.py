from molsysmt.form.file_dcd.is_file_dcd import is_file_dcd as is_form
from molsysmt.form.file_dcd.extract import extract
from molsysmt.form.file_dcd.add import add
from molsysmt.form.file_dcd.append_structures import append_structures
from molsysmt.form.file_dcd.get import *
from molsysmt.form.file_dcd.set import *
from .form_attributes import form_attributes

form_name = 'file:dcd'
form_type = 'file'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['coordinates'] = True
form_attributes['box'] = True

