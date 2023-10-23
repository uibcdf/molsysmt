form_name = 'molsysmt.Topology2'
form_type = 'class'
form_info = ["", ""]

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
from .iterators import TopologyIterator

from .to_file_msmh5 import to_file_msmh5

_convert_to={
        'molsysmt.Topology2': extract,
        'file:msmh5': to_file_msmh5,
        }
