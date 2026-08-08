form_name = 'parmed.Structure'
form_type = 'class'
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
        'parmed.Structure': 'to_parmed_Structure',
        'parmed.GromacsTopologyFile': 'to_parmed_GromacsTopologyFile',
        'file:mol2': 'to_file_mol2',
        'file:pdb': 'to_file_pdb',
        'file:psf': 'to_file_psf',
        'mdtraj.Topology': 'to_mdtraj_Topology',
        'mdtraj.Trajectory': 'to_mdtraj_Trajectory',
        'nglview.NGLWidget': 'to_nglview_NGLWidget',
        'openmm.Modeller': 'to_openmm_Modeller',
        'openmm.Topology': 'to_openmm_Topology',
        'molsysmt.MolSys': 'to_molsysmt_MolSys',
        'molsysmt.Topology': 'to_molsysmt_Topology',
        'molsysmt.Structures': 'to_molsysmt_Structures',
        }



piped_topological_attribute = 'molsysmt.Topology'
piped_structural_attribute = 'molsysmt.Structures'
piped_any_attribute = 'molsysmt.MolSys'
bonds_are_explicit = True
bonds_can_be_computed = False
