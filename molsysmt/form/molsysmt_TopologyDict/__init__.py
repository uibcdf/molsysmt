from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_molsysmt_TopologyDict import to_molsysmt_TopologyDict
from .to_file_topology_yaml import to_file_topology_yaml

form_name = 'molsysmt.TopologyDict'
form_type = 'class'
form_info = ['Declared, serializable topology representation.', '']

piped_topological_attribute = 'molsysmt.Topology'
piped_structural_attribute = None
piped_any_attribute = 'molsysmt.Topology'
bonds_are_explicit = True
bonds_can_be_computed = True

from .is_form import is_form
from .attributes import attributes
from .has_attribute import has_attribute
from .get_topological_attributes import *
from .get_structural_attributes import *

_convert_to = {
    'molsysmt.TopologyDict': to_molsysmt_TopologyDict,
    'molsysmt.Topology': to_molsysmt_Topology,
    'file:topology_yaml': to_file_topology_yaml,
}
