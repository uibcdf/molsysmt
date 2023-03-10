form_name = 'openmm.System'
form_type = 'class'
form_info = ["", ""]

from .is_form import is_form

from .attributes import attributes

from .extract import extract
from .copy import copy
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_openmm_Context import to_openmm_Context
from .to_openmm_Simulation import to_openmm_Simulation

_convert_to = {
        'openmm.Context': to_openmm_Context,
        'openmm.Simulation': to_openmm_Simulation,
        }
