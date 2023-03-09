form_name = 'molsysmt.Structures'
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
from .iterators import StructuresIterator, TopologyIterator

from .to_molsysmt_StructuresDict import to_molsysmt_StructuresDict, _to_molsysmt_StructuresDict
from .to_XYZ import to_XYZ, _to_XYZ

_convert_to={
        'molsysmt.StructuresDict': _to_molsysmt_StructuresDict,
        'XYZ': _to_XYZ,
        }
