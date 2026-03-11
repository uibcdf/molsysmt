from .to_molsysmt_MolSys import to_molsysmt_MolSys
from .to_molsysmt_MolSysBuilder import to_molsysmt_MolSysBuilder
from .to_molsysmt_MolSysDict import to_molsysmt_MolSysDict

form_name = "molsysmt.MolSysBuilder"
form_type = "class"
form_info = ["Editable native molecular system builder.", ""]

piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = True
bonds_can_be_computed = True

from .is_form import is_form
from .attributes import attributes
from .has_attribute import has_attribute
from .get_topological_attributes import *
from .get_structural_attributes import *
from .set import *

_convert_to = {
    "molsysmt.MolSysBuilder": "to_molsysmt_MolSysBuilder",
    "molsysmt.MolSys": "to_molsysmt_MolSys",
    "molsysmt.MolSysDict": "to_molsysmt_MolSysDict",
}
