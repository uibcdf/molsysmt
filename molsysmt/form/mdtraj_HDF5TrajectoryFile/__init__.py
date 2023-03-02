form_name = 'mdtraj.HDF5TrajectoryFile'
form_type = 'class'
form_info = ["", ""]

from .is_mdtraj_HDF5TrajectoryFile import is_mdtraj_HDF5TrajectoryFile

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_mdtraj_Topology import to_mdtraj_Topology, _to_mdtraj_Topology
from .to_openmm_Topology import to_openmm_Topology, _to_openmm_Topology
from .to_molsysmt_Topology import to_molsysmt_Topology, _to_molsysmt_Topology
from .to_molsysmt_Structures import to_molsysmt_Structures, _to_molsysmt_Structures
from .to_molsysmt_MolSys import to_molsysmt_MolSys, _to_molsysmt_MolSys

