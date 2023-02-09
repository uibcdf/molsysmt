import numpy as np
from molsysmt.form.MDAnalysis_Topology.is_MDAnalysis_Topology import is_MDAnalysis_Topology as is_form
from molsysmt.form.MDAnalysis_Topology.extract import extract
from molsysmt.form.MDAnalysis_Topology.add import add
from molsysmt.form.MDAnalysis_Topology.append_structures import append_structures
from molsysmt.form.MDAnalysis_Topology.get import *
from molsysmt.form.MDAnalysis_Topology.set import *
from molsysmt.form.MDAnalysis_Topology.iterators import StructuresIterator, TopologyIterator
from .form_attributes import form_attributes

form_name = 'MDAnalysis.Topology'
form_type = 'class'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['atom_index'] = True
form_attributes['atom_id'] = True
form_attributes['atom_name'] = True
form_attributes['atom_type'] = True
form_attributes['bond_index'] = True
form_attributes['bond_id'] = True
form_attributes['bond_name'] = True
form_attributes['bond_type'] = True
form_attributes['bond_order'] = True
form_attributes['group_index'] = True
form_attributes['group_id'] = True
form_attributes['group_name'] = True
form_attributes['group_type'] = True
form_attributes['component_index'] = True
form_attributes['molecule_index'] = True
form_attributes['molecule_id'] = True
form_attributes['molecule_name'] = True
form_attributes['molecule_type'] = True
form_attributes['chain_index'] = True
form_attributes['chain_id'] = True
form_attributes['chain_name'] = True
form_attributes['chain_type'] = True
