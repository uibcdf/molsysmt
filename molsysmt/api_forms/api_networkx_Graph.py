from molsysmt.form.networkx_Graph.is_networkx_Graph import is_networkx_Graph as is_form
from molsysmt.form.networkx_Graph.extract import extract
from molsysmt.form.networkx_Graph.add import add
from molsysmt.form.networkx_Graph.append_structures import append_structures
from molsysmt.form.networkx_Graph.get import *
from molsysmt.form.networkx_Graph.set import *
import numpy as np
from .form_attributes import form_attributes

form_name = 'networkx.Graph'
form_type = 'class'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['atom_index'] = True
form_attributes['bond_index'] = True
form_attributes['bonded_atoms'] = True
