form_name='molsysmt.StructuresDict'
form_type='class'
form_info = ["",""]

from .is_form import is_form

from .attributes import attributes
from .has_attribute import has_attribute

from .extract import extract
from .copy import copy
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator

from .to_molsysmt_Structures import to_molsysmt_Structures
from .to_file_trjpk import to_file_trjpk

_convert_to={
        'molsysmt.StructuresDict': extract,
        'molsysmt.Structures': to_molsysmt_Structures,
        'file:trjpk': to_file_trjpk,
        }
