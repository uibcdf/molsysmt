form_name = 'openmm.AmberPrmtopFile'
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

from .to_molsysmt_TopologyOld import to_molsysmt_TopologyOld
from .to_openmm_System import to_openmm_System
from .to_openmm_Topology import to_openmm_Topology

_convert_to={
        'openmm.AmberPrmtopFile': extract,
        'molsysmt.TopologyOld': to_molsysmt_TopologyOld,
        'openmm.System': to_openmm_System,
        'openmm.Topology': to_openmm_Topology,
        }
