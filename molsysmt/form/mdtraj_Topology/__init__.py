form_name = 'mdtraj.Topology'
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
from .get_topological_attributes import *
from .get_structural_attributes import *
from .set import *
from .iterators import TopologyIterator

from .to_file_top import to_file_top
from .to_string_amino_acids_1 import to_string_amino_acids_1
from .to_string_amino_acids_3 import to_string_amino_acids_3
from .to_mdtraj_Trajectory import to_mdtraj_Trajectory
from .to_parmed_Structure import to_parmed_Structure
from .to_parmed_GromacsTopologyFile import to_parmed_GromacsTopologyFile
from .to_molsysmt_Topology import to_molsysmt_Topology
from .to_molsysmt_TopologyOld import to_molsysmt_TopologyOld
from .to_openmm_Topology import to_openmm_Topology

_convert_to={
        'mdtraj.Topology': extract,
        'file:top': to_file_top,
        'string:amino_acids_1': to_string_amino_acids_1,
        'string:amino_acids_3': to_string_amino_acids_3,
        'mdtraj_Trajectory': to_mdtraj_Trajectory,
        'parmed_Structure': to_parmed_Structure,
        'parmed_GromacsTopologyFile': to_parmed_GromacsTopologyFile,
        'molsysmt_Topology': to_molsysmt_Topology,
        'molsysmt_TopologyOld': to_molsysmt_TopologyOld,
        'openmm_Topology': to_openmm_Topology,
        }
