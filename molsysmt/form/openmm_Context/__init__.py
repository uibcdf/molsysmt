form_name = 'openmm.Context'
form_type = 'class'
form_info = ["", ""]

piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = False
bonds_can_be_computed = False

from .is_form import is_form

from .attributes import attributes
from .has_attribute import has_attribute

from .extract import extract
from .copy import copy
from .add import add
from .merge import merge
from .append_structures import append_structures
from .get_topological_attributes import *
from .get_structural_attributes import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_openmm_System import to_openmm_System
from .to_molsysmt_Structures import to_molsysmt_Structures

_convert_to={
        'openmm.Context': extract,
        'openmm.System': to_openmm_System,
        'molsysmt.Structures': to_molsysmt_Structures,
        }
