"""Supporting one explicit SDF connection table without optional dependencies."""

from .attributes import attributes
from .copy import copy
from .extract import extract
from .get_structural_attributes import get_n_structures_from_system
from .get_topological_attributes import get_n_atoms_from_system
from .has_attribute import has_attribute
from .is_form import is_form

form_name = "file:sdf"
form_type = "file"
form_info = [
    "Single-record native SDF (V2000/V3000)",
    "https://discover.3ds.com/ctfile-documentation-request-form",
]
piped_topological_attribute = "molsysmt.Topology"
piped_structural_attribute = "molsysmt.Structures"
piped_any_attribute = "molsysmt.MolSys"
bonds_are_explicit = True
bonds_can_be_computed = False

_convert_to = {
    "molsysmt.MolSys": "to_molsysmt_MolSys",
    "molsysmt.Topology": "to_molsysmt_Topology",
    "molsysmt.Structures": "to_molsysmt_Structures",
    "file:sdf": "to_file_sdf",
}

_conversion_opt_kwargs = {
    "molsysmt.MolSys": ["discard_properties"],
    "molsysmt.Topology": ["discard_properties"],
    "molsysmt.Structures": ["discard_properties"],
    "file:sdf": ["ctfile_version", "discard_properties"],
}
