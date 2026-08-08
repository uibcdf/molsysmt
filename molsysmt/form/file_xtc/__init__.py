form_name = 'file:xtc'
form_type = 'file'
form_info = ["", ""]

piped_topological_attribute = None
piped_structural_attribute = 'mdtraj.XTCTrajectoryFile'
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
from .iterators import StructuresIterator


_convert_to={
        'file:xtc': 'to_file_xtc',
        'mdtraj.Trajectory': 'to_mdtraj_Trajectory',
        'mdtraj.XTCTrajectoryFile': 'to_mdtraj_XTCTrajectoryFile',
        'molsysmt.Structures': 'to_molsysmt_Structures',
        'file:h5msm': 'to_file_h5msm',
        }
_heavy_support = {
    'coordinates': True,
    'box': True,
}
bonds_are_explicit = False
bonds_can_be_computed = False
