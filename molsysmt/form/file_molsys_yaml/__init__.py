from depdigest import is_installed

form_name = 'file:molsys_yaml'
form_type = 'file'
form_info = ['Human-authored declarative YAML molecular system file.', '']

piped_topological_attribute = 'molsysmt.MolSys'
piped_structural_attribute = 'molsysmt.MolSys'
piped_any_attribute = 'molsysmt.MolSys'
bonds_are_explicit = True
bonds_can_be_computed = True

from .is_form import is_form
from .attributes import attributes
from .has_attribute import has_attribute
from .get_topological_attributes import *
from .get_structural_attributes import *

_convert_to = {}
if is_installed('yaml'):
    _convert_to = {
        'file:molsys_yaml': 'to_file_molsys_yaml',
        'molsysmt.MolSysDict': 'to_molsysmt_MolSysDict',
        'molsysmt.MolSys': 'to_molsysmt_MolSys',
    }
