from molsysmt.form.MDAnalysis_topology_CRDParser.is_MDAnalysis_topology_CRDParser import is_MDAnalysis_topology_CRDParser as is_form
from molsysmt.form.MDAnalysis_topology_CRDParser.extract import extract
from molsysmt.form.MDAnalysis_topology_CRDParser.add import add
from molsysmt.form.MDAnalysis_topology_CRDParser.append_structures import append_structures
from molsysmt.form.MDAnalysis_topology_CRDParser.get import *
from molsysmt.form.MDAnalysis_topology_CRDParser.set import *
from molsysmt.form.MDAnalysis_topology_CRDParser.iterators import StructuresIterator, TopologyIterator
from .form_attributes import form_attributes

form_name = 'MDAnalysis.topology.CRDParser'
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

