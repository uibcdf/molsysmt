form_name = "string:smiles"
form_type = "string"
form_info = [
    "SMILES (Simplified Molecular Input Line Entry System) string",
    "https://en.wikipedia.org/wiki/Simplified_molecular-input_line-entry_system",
]

piped_topological_attribute = "molsysmt.Topology"
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = True
bonds_can_be_computed = True

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
from .set import *  # noqa: E402, F403
from .iterators import StructuresIterator, TopologyIterator  # noqa: E402
# isort: on


_convert_to = {
    "string:smiles": "to_string_smiles",
    "rdkit.Mol": "to_rdkit_Mol",
    "molsysmt.Topology": "to_molsysmt_Topology",
    "file:smi": "to_file_smi",
    "openff.Molecule": "to_openff_Molecule",
}
