"""Reading gzip PDB inputs through the shared native PDB parser."""

form_name = "file:pdb.gz"
form_type = "file"
form_info = [
    "Gzip-compressed Protein Data Bank file",
    "https://www.wwpdb.org/documentation/file-format-content/format33/v3.3.html",
]
piped_topological_attribute = "molsysmt.PDBFileHandler"
piped_structural_attribute = "molsysmt.PDBFileHandler"
piped_any_attribute = "molsysmt.PDBFileHandler"
bonds_are_explicit = True
bonds_can_be_computed = True

from .attributes import attributes  # noqa: E402
from .has_attribute import has_attribute  # noqa: E402
from .is_form import is_form  # noqa: E402

_convert_to = {
    "molsysmt.PDBFileHandler": "to_molsysmt_PDBFileHandler",
    "molsysmt.MolSys": "to_molsysmt_MolSys",
    "molsysmt.Topology": "to_molsysmt_Topology",
    "molsysmt.Structures": "to_molsysmt_Structures",
    "string:pdb_text": "to_string_pdb_text",
}
_conversion_opt_kwargs = {
    "molsysmt.MolSys": ["bond_inference_engine"],
    "molsysmt.Topology": ["bond_inference_engine"],
}
