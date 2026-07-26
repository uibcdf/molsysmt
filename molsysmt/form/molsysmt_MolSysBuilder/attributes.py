from molsysmt.attribute.attributes import attributes as _all_attributes
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
