form_name = "biopython.PDBStructure"
form_type = "class"
form_info = ["", ""]

piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = False
bonds_can_be_computed = True

_convert_to = {
    "molsysmt.MolSys": "to_molsysmt_MolSys",
    "molsysmt.Topology": "to_molsysmt_Topology",
    "molsysmt.Structures": "to_molsysmt_Structures",
}

# Form metadata and export initialization retain their established import order.
# isort: off
from .is_form import is_form  # noqa: E402
from .attributes import attributes  # noqa: E402
from .has_attribute import has_attribute  # noqa: E402

# from .get_topological_attributes import *
from .get_structural_attributes import *  # noqa: E402, F403
# isort: on
