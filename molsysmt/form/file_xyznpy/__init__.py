form_name = 'file:xyznpy'
form_type = 'file'
form_info = ["XYZ file format like saved with Numpy", ""]

from .is_form import is_form

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_XYZ import to_XYZ, _to_XYZ

_convert_to={
        'XYZ': _to_XYZ,
        }
