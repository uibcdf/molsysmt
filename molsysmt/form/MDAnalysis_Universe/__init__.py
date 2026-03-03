form_name = 'MDAnalysis.Universe'
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


_convert_to={
        'MDAnalysis.Universe': 'to_MDAnalysis_Universe',
        'mdtraj.Trajectory': 'to_mdtraj_Trajectory',
        'nglview.NGLWidget': 'to_nglview_NGLWidget',
        'file:pdb': 'to_file_pdb',
        'molsysmt.MolSys': 'to_molsysmt_MolSys',
        'molsysmt.Topology': 'to_molsysmt_Topology',
        'molsysmt.Structures': 'to_molsysmt_Structures',
        }
