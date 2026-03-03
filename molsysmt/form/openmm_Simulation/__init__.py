form_name = 'openmm.Simulation'
form_type = 'class'
form_info = ["", ""]

piped_topological_attribute = 'openmm.Topology'
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = True
bonds_can_be_computed = True

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
from .iterators import StructuresIterator, TopologyIterator


_convert_to={
        'openmm.Simulation': 'to_openmm_Simulation',
        'file:pdb': 'to_file_pdb',
        'file:msmpk': 'to_file_msmpk',
        'openmm.Context': 'to_openmm_Context',
        'openmm.Topology': 'to_openmm_Topology',
        'molsysmt.MolSys': 'to_molsysmt_MolSys',
        'molsysmt.Structures': 'to_molsysmt_Structures',
        'molsysmt.Topology': 'to_molsysmt_Topology',
        'openmm.Modeller': 'to_openmm_Modeller',
        'pdbfixer.PDBFixer': 'to_pdbfixer_PDBFixer',
        }
