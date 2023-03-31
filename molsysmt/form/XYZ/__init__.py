form_name = 'XYZ'
form_type = 'class'
form_info = ["", ""]

from .is_form import is_form
from .get_rank_3_XYZ import get_rank_3_XYZ

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

from .to_file_xyznpy import to_file_xyznpy
from .to_molsysmt_Structures import to_molsysmt_Structures

_convert_to={
        'XYZ': extract,
        'file:xyznpy': to_file_xyznpy,
        'molsysmt.Structures': to_molsysmt_Structures,
        }
