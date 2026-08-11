form_name = 'openmm.Modeller'
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
        'openmm.Modeller': 'to_openmm_Modeller',
        'file:pdb': 'to_file_pdb',
        'molsysmt.MolSys': 'to_molsysmt_MolSys',
        'molsysmt.Topology': 'to_molsysmt_Topology',
        'molsysmt.Structures': 'to_molsysmt_Structures',
        'mdtraj.Topology': 'to_mdtraj_Topology',
        'mdtraj.Trajectory': 'to_mdtraj_Trajectory',
        'openmm.System': 'to_openmm_System',
        'openmm.Simulation': 'to_openmm_Simulation',
        'openmm.Topology': 'to_openmm_Topology',
        'pdbfixer.PDBFixer': 'to_pdbfixer_PDBFixer',
        'nglview.NGLWidget': 'to_nglview_NGLWidget',
        }

_conversion_opt_kwargs={
        'openmm.Simulation': ['collisions_rate', 'integration_timestep'],
        }
