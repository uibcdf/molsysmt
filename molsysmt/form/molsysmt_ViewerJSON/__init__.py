form_name = "molsysmt.ViewerJSON"
form_type = "class"
form_info = ["", ""]

piped_topological_attribute = "molsysmt.MolSys"
piped_structural_attribute = "molsysmt.MolSys"
piped_any_attribute = "molsysmt.MolSys"
bonds_are_explicit = True
bonds_can_be_computed = True

__all__ = [
    "form_name",
    "form_type",
    "form_info",
    "piped_topological_attribute",
    "piped_structural_attribute",
    "piped_any_attribute",
    "bonds_are_explicit",
    "bonds_can_be_computed",
    "is_form",
    "attributes",
    "has_attribute",
    "copy",
    "extract",
    "append_structures",
    "_convert_to",
]

# Form metadata and export initialization retain their established import order.
# isort: off
from .is_form import is_form  # noqa: E402
from .attributes import attributes  # noqa: E402
from .has_attribute import has_attribute  # noqa: E402

from .get_topological_attributes import *  # noqa: E402, F403
from .get_structural_attributes import *  # noqa: E402, F403
from .copy import copy  # noqa: E402
from .extract import extract  # noqa: E402
from .append_structures import append_structures  # noqa: E402
# isort: on


_convert_to = {
    "molsysmt.ViewerJSON": "to_molsysmt_ViewerJSON",
    "molsysmt.MolSys": "to_molsysmt_MolSys",
}
