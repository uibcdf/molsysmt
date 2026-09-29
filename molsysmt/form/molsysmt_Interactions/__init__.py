form_name = "molsysmt.Interactions"
form_type = "class"
form_info = ["Sparse, typed interaction result.", ""]
piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = False
bonds_can_be_computed = False
provides_atom_domain = True

from .attributes import attributes  # noqa: E402
from .get_structural_attributes import *  # noqa: E402, F403
from .get_topological_attributes import *  # noqa: E402, F403
from .has_attribute import has_attribute  # noqa: E402
from .is_form import is_form  # noqa: E402

_convert_to = {
    "molsysmt.Interactions": "to_molsysmt_Interactions",
    "molsysmt.InteractionsDict": "to_molsysmt_InteractionsDict",
}
