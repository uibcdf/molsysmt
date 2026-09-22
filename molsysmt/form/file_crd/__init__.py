form_name = "file:crd"
form_type = "file"
form_info = [
    "CHARMM card (CRD) file format with coordinates.",
    "https://www.charmmtutorial.org/index.php/CHARMM:The_Basics#CHARMM_data_structures",
]

piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None

# Form metadata and export initialization retain their established import order.
# isort: off
from .is_form import is_form  # noqa: E402

from .attributes import attributes  # noqa: E402
from .has_attribute import has_attribute  # noqa: E402

from .extract import extract  # noqa: E402
from .copy import copy  # noqa: E402
from .add import add  # noqa: E402
from .merge import merge  # noqa: E402
from .append_structures import append_structures  # noqa: E402
from .get_topological_attributes import *  # noqa: E402, F403
from .get_structural_attributes import *  # noqa: E402, F403
from .set import *  # noqa: E402, F403
from .iterators import StructuresIterator, TopologyIterator  # noqa: E402
# isort: on


_convert_to = {
    "file:crd": "to_file_crd",
    "molsysmt.MolSys": "to_molsysmt_MolSys",
    "molsysmt.Topology": "to_molsysmt_Topology",
    "molsysmt.Structures": "to_molsysmt_Structures",
    "openmm.CharmmCrdFile": "to_openmm_CharmmCrdFile",
}


piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = False
bonds_can_be_computed = False
