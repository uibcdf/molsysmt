form_name = 'file:xyznpy'
form_type = 'file'
form_info = ["XYZ file format like saved with Numpy", ""]

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

from .to_XYZ import to_XYZ 

_convert_to={
        'file:xyznpy': extract,
        'XYZ': to_XYZ,
        }
