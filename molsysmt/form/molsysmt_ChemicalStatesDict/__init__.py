form_name = "molsysmt.ChemicalStatesDict"
form_type = "class"
form_info = ["Versioned typed columns for chemical states.", ""]
piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = True
bonds_can_be_computed = False
provides_primary_topology = False
provides_atom_domain = True

from .attributes import attributes  # noqa: E402
from .get_topological_attributes import *  # noqa: E402, F403
from .has_attribute import has_attribute  # noqa: E402
from .is_form import is_form  # noqa: E402

_convert_to = {
    "molsysmt.ChemicalStatesDict": "to_molsysmt_ChemicalStatesDict",
    "molsysmt.ChemicalStates": "to_molsysmt_ChemicalStates",
}
