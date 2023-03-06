form_name = 'MDAnalysis.Topology'
form_type = 'class'
form_info = ["", ""]

from .is_MDAnalysis_Topology import is_MDAnalysis_Topology

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

_dict_convert={}
