form_name = 'file:mol2'
form_type = 'file'
form_info = ["", ""]

piped_topological_attribute = 'molsysmt.Topology'
piped_structural_attribute = 'molsysmt.Structures'
piped_any_attribute = 'molsysmt.MolSys'

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
from .get_mechanical_attributes import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator


_convert_to={
        'file:mol2': 'to_file_mol2',
        'file:pdb': 'to_file_pdb',
        'mdtraj.Trajectory': 'to_mdtraj_Trajectory',
        'mdtraj.Topology': 'to_mdtraj_Topology',
        'molsysmt.Topology': 'to_molsysmt_Topology',
        'molsysmt.Structures': 'to_molsysmt_Structures',
        'molsysmt.MolSys': 'to_molsysmt_MolSys',
        'openmm.Topology': 'to_openmm_Topology',
        'openmm.Modeller': 'to_openmm_Modeller',
        'parmed.Structure': 'to_parmed_Structure',
        'nglview.NGLWidget': 'to_nglview_NGLWidget',
        }


piped_topological_attribute = 'molsysmt.Topology'
piped_structural_attribute = 'molsysmt.Structures'
piped_any_attribute = 'molsysmt.MolSys'
bonds_are_explicit = True
bonds_can_be_computed = False
