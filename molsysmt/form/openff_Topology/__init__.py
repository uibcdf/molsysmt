form_name = 'openff.Topology'
form_type = 'class'
form_info = ["OpenFF Toolkit Topology", "https://docs.openforcefield.org/projects/toolkit/"]

piped_topological_attribute = 'molsysmt.Topology'
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = True
bonds_can_be_computed = True

_convert_to = {
    'molsysmt.Topology': 'to_molsysmt_Topology',
    'molsysmt.Structures': 'to_molsysmt_Structures',
    'molsysmt.MolSys': 'to_molsysmt_MolSys',
    'openff.Molecule': 'to_openff_Molecule',
    'openmm.Topology': 'to_openmm_Topology',
}

from .is_form import is_form
from .attributes import attributes
from .has_attribute import has_attribute
from .extract import extract
from .copy import copy
from .add import add
from .merge import merge
from .get_topological_attributes import *
from .get_structural_attributes import *
from .get_mechanical_attributes import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator
