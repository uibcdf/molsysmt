form_name = 'openmm.GromacsTopFile'
form_type = 'class'
form_info = ["", ""]

piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None

from .is_form import is_form

from .attributes import attributes
from .has_attribute import has_attribute

from .extract import extract
from .copy import copy
from .add import add
from .merge import merge
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import TopologyIterator

from .to_openmm_Topology import to_openmm_Topology
from .to_molsysmt_TopologyOld import to_molsysmt_TopologyOld

_convert_to={
        'openmm.GromacsTopFile': extract,
        'openmm.Topology': to_openmm_Topology,
        'molsysmt.TopologyOld': to_molsysmt_TopologyOld,
        }
