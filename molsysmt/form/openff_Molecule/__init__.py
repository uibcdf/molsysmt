form_name = "openff.Molecule"
form_type = "class"
form_info = [
    "OpenFF Toolkit Molecule",
    "https://docs.openforcefield.org/projects/toolkit/",
]

piped_topological_attribute = "molsysmt.Topology"
piped_structural_attribute = "molsysmt.Structures"
piped_any_attribute = "molsysmt.MolSys"
bonds_are_explicit = True
bonds_can_be_computed = True

# Form metadata and export initialization must retain their established order.
# The wildcard imports expose the form's getter and setter functions.
# isort: off
from .extract import extract  # noqa: E402

_convert_to = {
    "openff.Molecule": extract,
    "molsysmt.Topology": "to_molsysmt_Topology",
    "molsysmt.Structures": "to_molsysmt_Structures",
    "molsysmt.MolSys": "to_molsysmt_MolSys",
    "openff.Topology": "to_openff_Topology",
    "rdkit.Mol": "to_rdkit_Mol",
    "string:smiles": "to_string_smiles",
}

from .is_form import is_form  # noqa: E402
from .attributes import attributes  # noqa: E402
from .has_attribute import has_attribute  # noqa: E402
from .copy import copy  # noqa: E402
from .add import add  # noqa: E402
from .merge import merge  # noqa: E402
from .get_topological_attributes import *  # noqa: E402, F403
from .get_structural_attributes import *  # noqa: E402, F403
from .get_mechanical_attributes import *  # noqa: E402, F403
from .set import *  # noqa: E402, F403
from .iterators import StructuresIterator, TopologyIterator  # noqa: E402
# isort: on
