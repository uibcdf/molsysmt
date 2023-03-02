form_name='molsysmt.StructuresDict'
form_type='class'
form_info = ["",""]

from .is_molsysmt_StructuresDict import is_molsysmt_StructuresDict

from .attributes import attributes
from .has_attribute import has_attribute

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_molsysmt_Structures import to_molsysmt_Structures, _to_molsysmt_Structures
from .to_file_trjpk import to_file_trjpk, _to_file_trjpk

