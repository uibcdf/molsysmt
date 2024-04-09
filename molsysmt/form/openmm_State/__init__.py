form_name = 'openmm.State'
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
from .iterators import StructuresIterator, TopologyIterator

from .to_XYZ import to_XYZ
from .to_molsysmt_StructuresOld import to_molsysmt_StructuresOld

_convert_to={
        'openmm.State': extract,
        'molsysmt.StructuresOld': to_molsysmt_StructuresOld,
        'XYZ': to_XYZ,
        }

