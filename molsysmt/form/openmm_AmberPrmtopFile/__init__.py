form_name = 'openmm.AmberPrmtopFile'
form_type = 'class'
form_info = ["", ""]

from .is_openmm_AmberPrmtopFile import is_openmm_AmberPrmtopFile

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_molsysmt_Topology import to_molsysmt_Topology, _to_molsysmt_Topology
from .to_openmm_System import to_openmm_System, _to_openmm_System
from .to_openmm_Topology import to_openmm_Topology, _to_openmm_Topology

_convert_to={
        'molsysmt.Topology': _to_molsysmt_Topology,
        'openmm.System': _to_openmm_System,
        'openmm.Topology': _to_openmm_Topology,
        }
