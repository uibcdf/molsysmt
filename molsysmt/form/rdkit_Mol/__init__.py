form_name = "rdkit.Mol"
form_type = "class"
form_info = ["", ""]

piped_topological_attribute = "molsysmt.Topology"
piped_structural_attribute = "molsysmt.Structures"
piped_any_attribute = "molsysmt.MolSys"
bonds_are_explicit = True
bonds_can_be_computed = True

_convert_to = {
    "rdkit.Mol": "extract",
    "molsysmt.MolSys": "to_molsysmt_MolSys",
    "molsysmt.Topology": "to_molsysmt_Topology",
    "molsysmt.Structures": "to_molsysmt_Structures",
    "string:smiles": "to_string_smiles",
    "file:smi": "to_file_smi",
    "openff.Molecule": "to_openff_Molecule",
}

# Form metadata and export initialization retain their established import order.
# isort: off
from .is_form import is_form  # noqa: E402
from .attributes import attributes  # noqa: E402
from .get_topological_attributes import *  # noqa: E402, F403
from .get_structural_attributes import *  # noqa: E402, F403
from .get_mechanical_attributes import *  # noqa: E402, F403
from .has_attribute import has_attribute  # noqa: E402
# isort: on
