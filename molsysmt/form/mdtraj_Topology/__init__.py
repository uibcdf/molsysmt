form_name = 'mdtraj.Topology'
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

from .to_file_top import to_file_top, _to_file_top
from .to_string_aminoacids1 import to_string_aminoacids1, _to_string_aminoacids1
from .to_string_aminoacids3 import to_string_aminoacids3, _to_string_aminoacids3
from .to_mdtraj_Trajectory import to_mdtraj_Trajectory, _to_mdtraj_Trajectory
from .to_parmed_Structure import to_parmed_Structure, _to_parmed_Structure
from .to_parmed_GromacsTopologyFile import to_parmed_GromacsTopologyFile, _to_parmed_GromacsTopologyFile
from .to_molsysmt_Topology import to_molsysmt_Topology, _to_molsysmt_Topology
from .to_openmm_Topology import to_openmm_Topology, _to_openmm_Topology

_convert_to={
        'file:top': _to_file_top,
        'string:aminoacids1': _to_string_aminoacids1,
        'string:aminoacids3': _to_string_aminoacids1,
        'mdtraj_Trajectory': _to_mdtraj_Trajectory,
        'parmed_Structure': _to_parmed_Structure,
        'parmed_GromacsTopologyFile': _to_parmed_GromacsTopologyFile,
        'molsysmt_Topology': _to_molsysmt_Topology,
        'openmm_Topology': _to_openmm_Topology,
        }
