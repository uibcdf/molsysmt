form_name = 'openmm.GromacsGroFile'
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

from .to_openmm_Topology import to_openmm_Topology
from .to_openmm_Modeller import to_openmm_Modeller
from .to_molsysmt_TopologyOld import to_molsysmt_TopologyOld
from .to_molsysmt_StructuresOld import to_molsysmt_StructuresOld
from .to_molsysmt_MolSysOld import to_molsysmt_MolSysOld

_convert_to={
        'openmm.GromacsGroFile': extract,
        'openmm.Topology': to_openmm_Topology,
        'openmm.Modeller': to_openmm_Modeller,
        'molsysmt.TopologyOld': to_molsysmt_TopologyOld,
        'molsysmt.StructuresOld': to_molsysmt_StructuresOld,
        'molsysmt.MolSysOld': to_molsysmt_MolSysOld
        }
