form_name = 'pytraj.Topology'
form_type = 'class'
form_info = ["", ""]

from .is_form import is_form

from .attributes import attributes

from .extract import extract
from .copy import copy
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_pytraj_Trajectory import to_pytraj_Trajectory

_convert_to={
        'molsysmt.Topology': to_molsysmt_Topology,
        'pytraj.Trajectory': to_pytraj_Trajectory,
        }
