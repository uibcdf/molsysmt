form_name = "openff.Topology"
form_type = "class"
form_info = [
    "OpenFF Toolkit Topology",
    "https://docs.openforcefield.org/projects/toolkit/",
]

piped_topological_attribute = "molsysmt.Topology"
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = True
bonds_can_be_computed = True

_convert_to = {
    "molsysmt.Topology": "to_molsysmt_Topology",
    "molsysmt.Structures": "to_molsysmt_Structures",
    "molsysmt.MolSys": "to_molsysmt_MolSys",
    "openff.Molecule": "to_openff_Molecule",
    "openmm.Topology": "to_openmm_Topology",
}

# Form metadata and export initialization must retain their established order.
# The wildcard imports expose the form's getter and setter functions.
# isort: off
from .is_form import is_form  # noqa: E402
from .attributes import attributes  # noqa: E402
from .has_attribute import has_attribute  # noqa: E402
from .extract import extract  # noqa: E402
from .copy import copy  # noqa: E402
from .add import add  # noqa: E402
from .merge import merge  # noqa: E402
from .get_topological_attributes import *  # noqa: E402, F403
from .get_structural_attributes import *  # noqa: E402, F403
from .get_mechanical_attributes import *  # noqa: E402, F403
from .set import *  # noqa: E402, F403
from .iterators import StructuresIterator, TopologyIterator  # noqa: E402
# isort: on
