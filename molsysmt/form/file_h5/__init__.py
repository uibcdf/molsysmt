form_name = 'file:h5'
form_type = 'file'
form_info = ["", ""]

piped_topological_attribute = None
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
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator


_convert_to={
        'file:h5': 'to_file_h5',
        'mdtraj.HDF5TrajectoryFile': 'to_mdtraj_HDF5TrajectoryFile',
        'molsysmt.MolSys': 'to_molsysmt_MolSys',
        'molsysmt.Topology': 'to_molsysmt_Topology',
        'molsysmt.Structures': 'to_molsysmt_Structures',
        'nglview.NGLWidget': 'to_nglview_NGLWidget',
        'openmm.Topology': 'to_openmm_Topology',
        'mdtraj.Topology': 'to_mdtraj_Topology',
        'mdtraj.Trajectory': 'to_mdtraj_Trajectory',
        'file:pdb': 'to_file_pdb',
        }
