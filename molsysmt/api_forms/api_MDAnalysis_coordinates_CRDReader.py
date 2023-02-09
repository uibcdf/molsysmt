from molsysmt.form.MDAnalysis_coordinates_CRDReader.is_MDAnalysis_coordinates_CRDReader import is_MDAnalysis_coordinates_CRDReader as is_form
from molsysmt.form.MDAnalysis_coordinates_CRDReader.extract import extract
from molsysmt.form.MDAnalysis_coordinates_CRDReader.add import add
from molsysmt.form.MDAnalysis_coordinates_CRDReader.append_structures import append_structures
from molsysmt.form.MDAnalysis_coordinates_CRDReader.get import *
from molsysmt.form.MDAnalysis_coordinates_CRDReader.set import *
from molsysmt.form.MDAnalysis_coordinates_CRDReader.iterators import StructuresIterator, TopologyIterator
from .form_attributes import form_attributes

form_name = 'MDAnalysis.coordinates.CRDReader'
form_type = 'class'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['atom_index'] = True
form_attributes['coordinates'] = True
form_attributes['box'] = True

