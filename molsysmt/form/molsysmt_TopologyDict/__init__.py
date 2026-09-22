form_name = "molsysmt.TopologyDict"
form_type = "class"
form_info = ["Declared, serializable topology representation.", ""]

piped_topological_attribute = "molsysmt.Topology"
piped_structural_attribute = None
piped_any_attribute = "molsysmt.Topology"
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
    "molsysmt.TopologyDict": "to_molsysmt_TopologyDict",
    "molsysmt.Topology": "to_molsysmt_Topology",
    "file:topology_yaml": "to_file_topology_yaml",
}
