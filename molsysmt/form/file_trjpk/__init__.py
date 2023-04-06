form_name='file:trjpk'
form_type='file'
form_info = ["",""]

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
from .iterators import StructuresIterator

from .to_molsysmt_StructuresDict import to_molsysmt_StructuresDict

_convert_to={
        'file:trjpk': extract,
        'molsysmt.StructuresDict': to_molsysmt_StructuresDict,
        }
