form_name = 'openmm.GromacsGroFile'
form_type = 'class'
form_info = ["", ""]

from .is_openmm_GromacsGroFile import is_openmm_GromacsGroFile

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_openmm_Topology import to_openmm_Topology, _to_openmm_Topology
from .to_openmm_Modeller import to_openmm_Modeller, _to_openmm_Modeller
from .to_molsysmt_Topology import to_molsysmt_Topology, _to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures, _to_molsysmt_Structures
from .to_molsysmt_MolSys import to_molsysmt_MolSys, _to_molsysmt_MolSys

