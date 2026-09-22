form_name = "molsysmt.MolSysDict"
form_type = "class"
form_info = ["Declarative serializable molecular system dictionary.", ""]

piped_topological_attribute = "molsysmt.MolSys"
piped_structural_attribute = "molsysmt.MolSys"
piped_any_attribute = "molsysmt.MolSys"
bonds_are_explicit = True
bonds_can_be_computed = True

# Form metadata and export initialization retain their established import order.
# isort: off
from .is_form import is_form  # noqa: E402
from .attributes import attributes  # noqa: E402
from .has_attribute import has_attribute  # noqa: E402
from .extract import extract  # noqa: E402
from .get_topological_attributes import *  # noqa: E402, F403
from .get_structural_attributes import *  # noqa: E402, F403
# isort: on

_convert_to = {
    "molsysmt.MolSysDict": "to_molsysmt_MolSysDict",
    "molsysmt.MolSysBuilder": "to_molsysmt_MolSysBuilder",
    "molsysmt.MolSys": "to_molsysmt_MolSys",
    "file:molsys_yaml": "to_file_molsys_yaml",
}
