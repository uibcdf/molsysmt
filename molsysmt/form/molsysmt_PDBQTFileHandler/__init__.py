"""Adapting resident or indexed PDBQT documents through native contracts."""

from .attributes import attributes
from .copy import copy
from .extract import extract
from .get_mechanical_attributes import *  # noqa: F403
from .get_structural_attributes import *  # noqa: F403
from .has_attribute import has_attribute
from .is_form import is_form
from .iterators import StructuresIterator, TopologyIterator

form_name = "molsysmt.PDBQTFileHandler"
_heavy_support = {"coordinates": True}
form_type = "class"
form_info = ["Validated resident or indexed PDBQT document", ""]
piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = False
bonds_can_be_computed = False

_convert_to = {
    "molsysmt.PDBQTFileHandler": "to_molsysmt_PDBQTFileHandler",
    "molsysmt.MolSys": "to_molsysmt_MolSys",
    "molsysmt.Topology": "to_molsysmt_Topology",
    "molsysmt.Structures": "to_molsysmt_Structures",
    "molsysmt.MolecularMechanics": "to_molsysmt_MolecularMechanics",
    "file:pdbqt": "to_file_pdbqt",
    "string:pdbqt_text": "to_string_pdbqt_text",
}
_conversion_opt_kwargs = {
    "molsysmt.MolSys": ["discard_torsion_tree"],
    "molsysmt.Topology": ["discard_torsion_tree"],
    "molsysmt.Structures": ["discard_torsion_tree"],
    "molsysmt.MolecularMechanics": ["discard_torsion_tree"],
}

from .get_topological_attributes import *  # noqa: E402, F403
