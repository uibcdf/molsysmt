from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_molsysmt_MolSysBuilder import to_molsysmt_MolSysBuilder
from .to_molsysmt_MolSysDict import to_molsysmt_MolSysDict
from .to_file_molsys_yaml import to_file_molsys_yaml

form_name = 'molsysmt.MolSysDict'
form_type = 'class'
form_info = ['Declarative serializable molecular system dictionary.', '']

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

_convert_to = {
    'molsysmt.MolSysDict': to_molsysmt_MolSysDict,
    'molsysmt.MolSysBuilder': to_molsysmt_MolSysBuilder,
    'molsysmt.MolSys': to_molsysmt_MolSys,
    'file:molsys_yaml': to_file_molsys_yaml,
}
