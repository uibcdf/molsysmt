from molsysmt.item.openmm_AmberInpcrdFile.is_openmm_AmberInpcrdFile import is_openmm_AmberInpcrdFile as is_form
from molsysmt.item.openmm_AmberInpcrdFile.extract import extract
from molsysmt.item.openmm_AmberInpcrdFile.add import add
from molsysmt.item.openmm_AmberInpcrdFile.append_structures import append_structures
from molsysmt.item.openmm_AmberInpcrdFile.get import *
from molsysmt.item.openmm_AmberInpcrdFile.set import *
from .form_attributes import form_attributes

form_name = 'openmm.AmberInpcrdFile'
form_type = 'class'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['coordinates'] = True
form_attributes['box'] = True
