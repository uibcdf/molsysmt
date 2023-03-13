form_name = 'openmm.AmberPrmtopFile'
form_type = 'class'
form_info = ["", ""]

from .is_form import is_form

from .attributes import attributes
from .has_attribute import has_attribute

from .extract import extract
from .copy import copy
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import TopologyIterator

from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_openmm_System import to_openmm_System
from .to_openmm_Topology import to_openmm_Topology

_convert_to={
        'molsysmt.Topology': to_molsysmt_Topology,
        'openmm.System': to_openmm_System,
        'openmm.Topology': to_openmm_Topology,
        }
