from depdigest import is_installed

from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_molsysmt_StructuresDict import to_molsysmt_StructuresDict
from .to_file_structures_yaml import to_file_structures_yaml

form_name = 'file:structures_yaml'
form_type = 'file'
form_info = ['Human-authored declarative YAML structures file.', '']

piped_topological_attribute = None
piped_structural_attribute = 'molsysmt.StructuresDict'
piped_any_attribute = 'molsysmt.StructuresDict'
bonds_are_explicit = False
bonds_can_be_computed = False

from .is_form import is_form
from .attributes import attributes
from .has_attribute import has_attribute
from .get_topological_attributes import *
from .get_structural_attributes import *

_convert_to = {}
if is_installed('yaml'):
    _convert_to = {
        'file:structures_yaml': to_file_structures_yaml,
        'molsysmt.StructuresDict': to_molsysmt_StructuresDict,
        'molsysmt.Structures': to_molsysmt_Structures,
    }
