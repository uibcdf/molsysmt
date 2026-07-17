form_name = 'MDAnalysis.AtomGroup'
form_type = 'class'
form_info = ["", ""]

piped_topological_attribute = 'molsysmt.Topology'
piped_structural_attribute = 'molsysmt.MolSys'
piped_any_attribute = 'molsysmt.MolSys'
bonds_are_explicit = True
bonds_can_be_computed = True

_convert_to = {
    'MDAnalysis.AtomGroup': 'extract',
    'molsysmt.MolSys': 'to_molsysmt_MolSys',
    'molsysmt.Topology': 'to_molsysmt_Topology',
    'MDAnalysis.Universe': 'to_MDAnalysis_Universe',
}

from .is_form import is_form
from .attributes import attributes
from .get_topological_attributes import *
from .get_structural_attributes import *
from .has_attribute import has_attribute
from .extract import extract
