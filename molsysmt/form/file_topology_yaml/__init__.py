from depdigest import is_installed

from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_molsysmt_TopologyDict import to_molsysmt_TopologyDict
from .to_file_topology_yaml import to_file_topology_yaml

form_name = 'file:topology_yaml'
form_type = 'file'
form_info = ['Human-authored declarative YAML topology file.', '']

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

_convert_to = {}
if is_installed('yaml'):
    _convert_to = {
        'file:topology_yaml': to_file_topology_yaml,
        'molsysmt.TopologyDict': to_molsysmt_TopologyDict,
        'molsysmt.Topology': to_molsysmt_Topology,
    }
