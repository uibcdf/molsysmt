form_name = 'mdtraj.HDF5TrajectoryFile'
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
        'mdtraj.HDF5TrajectoryFile': 'to_mdtraj_HDF5TrajectoryFile',
        'mdtraj.Topology': 'to_mdtraj_Topology',
        'openmm.Topology': 'to_openmm_Topology',
        'molsysmt.MolSys': 'to_molsysmt_MolSys',
        'molsysmt.Topology': 'to_molsysmt_Topology',
        'molsysmt.Structures': 'to_molsysmt_Structures',
        }
