form_name = 'openmm.Context'
form_type = 'class'
form_info = ["", ""]

from .is_form import is_form

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_openmm_System import to_openmm_System, _to_openmm_System
from .to_molsysmt_Structures import to_molsysmt_Structures, _to_molsysmt_Structures

_convert_to={
        'openmm.System': _to_openmm_System,
        'molsysmt.Structures': _to_molsysmt_Structures,
        }
