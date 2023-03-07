form_name = 'openmm.System'
form_type = 'class'
form_info = ["", ""]

from .is_openmm_System import is_openmm_System

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_openmm_Context import to_openmm_Context, _to_openmm_Context
from .to_openmm_Simulation import to_openmm_Simulation, _to_openmm_Simulation

_convert_to = {
        'openmm.Context': _to_openmm_Context,
        'openmm.Simulation': _to_openmm_Simulation,
        }
