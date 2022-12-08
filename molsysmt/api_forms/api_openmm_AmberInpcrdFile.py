from molsysmt.form.openmm_AmberInpcrdFile.is_openmm_AmberInpcrdFile import is_openmm_AmberInpcrdFile as is_form
from molsysmt.form.openmm_AmberInpcrdFile.extract import extract
from molsysmt.form.openmm_AmberInpcrdFile.add import add
from molsysmt.form.openmm_AmberInpcrdFile.append_structures import append_structures
from molsysmt.form.openmm_AmberInpcrdFile.get import *
from molsysmt.form.openmm_AmberInpcrdFile.set import *
from molsysmt.form.openmm_AmberInpcrdFile.iterators import StructuresIterator, TopologyIterator
from .form_attributes import form_attributes

form_name = 'openmm.AmberInpcrdFile'
form_type = 'class'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['coordinates'] = True
form_attributes['box'] = True
