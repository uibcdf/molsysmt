from molsysmt.form.openmm_CharmmCrdFile.is_openmm_CharmmCrdFile import is_openmm_CharmmCrdFile as is_form
from molsysmt.form.openmm_CharmmCrdFile.extract import extract
from molsysmt.form.openmm_CharmmCrdFile.add import add
from molsysmt.form.openmm_CharmmCrdFile.append_structures import append_structures
from molsysmt.form.openmm_CharmmCrdFile.get import *
from molsysmt.form.openmm_CharmmCrdFile.set import *
from molsysmt.form.openmm_CharmmCrdFile.iterators import StructuresIterator, TopologyIterator
from .form_attributes import form_attributes

form_name = 'openmm.CharmmCrdFile'
form_type = 'class'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['atom_index'] = True
form_attributes['atom_id'] = True
form_attributes['atom_name'] = True
form_attributes['atom_type'] = True
form_attributes['group_index'] = True
form_attributes['group_id'] = True
form_attributes['group_name'] = True
form_attributes['group_type'] = True
form_attributes['coordinates'] = True
form_attributes['box'] = True
