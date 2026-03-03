from .to_pytraj_Trajectory import to_pytraj_Trajectory
from .to_pytraj_Topology import to_pytraj_Topology
from .to_molsysmt_Topology import to_molsysmt_Topology
form_name = 'pytraj.Topology'
form_type = 'class'
form_info = ["", ""]

piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None

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
from .iterators import StructuresIterator, TopologyIterator


_convert_to={
        'pytraj.Topology': to_pytraj_Topology,
        'molsysmt.Topology': to_molsysmt_Topology,
        'pytraj.Trajectory': to_pytraj_Trajectory,
        }
