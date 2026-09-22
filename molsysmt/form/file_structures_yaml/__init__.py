# Form metadata and export initialization retain their established import order.
# isort: off
from depdigest import is_installed

form_name = "file:structures_yaml"
form_type = "file"
form_info = ["Human-authored declarative YAML structures file.", ""]

piped_topological_attribute = None
piped_structural_attribute = "molsysmt.StructuresDict"
piped_any_attribute = "molsysmt.StructuresDict"
bonds_are_explicit = False
bonds_can_be_computed = False

from .is_form import is_form  # noqa: E402
from .attributes import attributes  # noqa: E402
from .has_attribute import has_attribute  # noqa: E402
from .get_topological_attributes import *  # noqa: E402, F403
from .get_structural_attributes import *  # noqa: E402, F403
# isort: on

_convert_to = {}
if is_installed("yaml"):
    _convert_to = {
        "file:structures_yaml": "to_file_structures_yaml",
        "molsysmt.StructuresDict": "to_molsysmt_StructuresDict",
        "molsysmt.Structures": "to_molsysmt_Structures",
    }
