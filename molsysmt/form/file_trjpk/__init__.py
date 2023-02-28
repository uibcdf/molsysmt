form_name='file:trjpk'
form_type='file'
form_info = ["",""]

from .is_file_trjpk import is_file_trjpk

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_molsysmt_StructuresDict import to_molsysmt_StructuresDict

