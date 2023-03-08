form_name = 'openmm.GromacsTopFile'
form_type = 'class'
form_info = ["", ""]

from .is_form import is_form

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_openmm_Topology import to_openmm_Topology, _to_openmm_Topology
from .to_molsysmt_Topology import to_molsysmt_Topology, _to_molsysmt_Topology

_convert_to={
        'openmm.Topology': _to_openmm_Topology,
        'molsysmt.Topology': _to_molsysmt_Topology,
        }
