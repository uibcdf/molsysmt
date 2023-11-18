form_name = 'mdtraj.Topology'
form_type = 'class'
form_info = ["", ""]

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
from .iterators import TopologyIterator

from .to_file_top import to_file_top
from .to_string_aminoacids1 import to_string_aminoacids1
from .to_string_aminoacids3 import to_string_aminoacids3
from .to_mdtraj_Trajectory import to_mdtraj_Trajectory
from .to_parmed_Structure import to_parmed_Structure
from .to_parmed_GromacsTopologyFile import to_parmed_GromacsTopologyFile
from .to_molsysmt_TopologyOld import to_molsysmt_TopologyOld
from .to_openmm_Topology import to_openmm_Topology

_convert_to={
        'mdtraj.Topology': extract,
        'file:top': to_file_top,
        'string:aminoacids1': to_string_aminoacids1,
        'string:aminoacids3': to_string_aminoacids1,
        'mdtraj_Trajectory': to_mdtraj_Trajectory,
        'parmed_Structure': to_parmed_Structure,
        'parmed_GromacsTopologyFile': to_parmed_GromacsTopologyFile,
        'molsysmt_TopologyOld': to_molsysmt_TopologyOld,
        'openmm_Topology': to_openmm_Topology,
        }
