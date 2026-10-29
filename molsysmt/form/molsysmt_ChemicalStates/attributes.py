from molsysmt.attribute.attributes import attributes as _all_attributes
from molsysmt.native._chemical_fields import ATOM_FIELDS, BOND_FIELDS, COMPONENT_FIELDS

attributes = {name: False for name in _all_attributes}
for name in (
    "n_atoms",
    "n_chemical_states",
    "reference_chemical_state_index",
    "chemical_state_index",
    "chemical_state_id",
    "atom_index",
    "bond_index",
    "component_index",
    "n_bonds",
    "n_components",
    "connectivity_completeness",
    "component_completeness",
    "component_evidence",
):
    attributes[name] = True
for name in (*ATOM_FIELDS, *BOND_FIELDS, *COMPONENT_FIELDS):
    attributes[name] = True
