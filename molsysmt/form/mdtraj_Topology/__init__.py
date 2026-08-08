form_name = 'mdtraj.Topology'
form_type = 'class'
form_info = ["", ""]

piped_topological_attribute = 'molsysmt.Topology'
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


_convert_to={
        'mdtraj.Topology': 'to_mdtraj_Topology',
        'file:top': 'to_file_top',
        'string:amino_acids_1': 'to_string_amino_acids_1',
        'string:amino_acids_3': 'to_string_amino_acids_3',
        'mdtraj.Trajectory': 'to_mdtraj_Trajectory',
        'parmed.Structure': 'to_parmed_Structure',
        'parmed.GromacsTopologyFile': 'to_parmed_GromacsTopologyFile',
        'molsysmt.Topology': 'to_molsysmt_Topology',
        'openmm.Topology': 'to_openmm_Topology',
        }


piped_topological_attribute = 'molsysmt.Topology'
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = True
bonds_can_be_computed = False
