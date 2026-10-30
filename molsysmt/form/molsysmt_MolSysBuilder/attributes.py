from molsysmt.attribute.attributes import attributes as _all_attributes
from molsysmt.form.molsysmt_ChemicalStates.attributes import attributes as _chemistry
from molsysmt.form.molsysmt_Structures.attributes import (
    attributes as _structural_attributes,
)
from molsysmt.form.molsysmt_Topology.attributes import (
    attributes as _topological_attributes,
)

attributes = {
    name: bool(_topological_attributes[name] or _structural_attributes[name])
    for name in _all_attributes
}

del _all_attributes, _structural_attributes, _topological_attributes


for _name, _available in _chemistry.items():
    attributes[_name] = attributes.get(_name, False) or _available
attributes["structure_chemical_state_index"] = True

# These selection-dependent relations are delivered through the borrowed MolSys view.
for _name in ("inner_bond_index", "inner_bonded_atoms", "n_inner_bonds"):
    attributes[_name] = True
