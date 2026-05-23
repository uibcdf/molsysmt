from .to_XYZ import to_XYZ
from .to_molsysmt_Structures import to_molsysmt_Structures

form_name = 'cupy_ndarray'
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
from .iterators import *

_convert_to = {
    'XYZ': to_XYZ,
    'molsysmt.Structures': to_molsysmt_Structures,
}
