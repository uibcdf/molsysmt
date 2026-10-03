"""Supporting explicit AutoDock4 PDBQT records without chemical preparation."""

from .attributes import attributes
from .copy import copy
from .extract import extract
from .get_atom_ff_type_from_atom import get_atom_ff_type_from_atom
from .get_n_atoms_from_system import get_n_atoms_from_system
from .get_n_structures_from_system import get_n_structures_from_system
from .get_partial_charge_from_atom import get_partial_charge_from_atom
from .get_torsion_tree import get_torsion_tree
from .has_attribute import has_attribute
from .is_form import is_form

form_name = "file:pdbqt"
form_type = "file"
form_info = ["Bounded AutoDock4 PDBQT profile", "https://autodock.scripps.edu/"]
piped_topological_attribute = "molsysmt.Topology"
piped_structural_attribute = "molsysmt.Structures"
# A full MolSys projection requires explicit authorization to omit a ligand tree.
# Queries use reduced domain projections and direct mechanical getters instead.
piped_any_attribute = None
bonds_are_explicit = False
bonds_can_be_computed = False

_convert_to = {
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
